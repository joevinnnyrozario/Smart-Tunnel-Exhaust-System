/*
 * ESP8266 MQTT Sensor Node for Tunnel Exhaust System
 *
 * Collects data from:
 * 1. DHT11 (Temperature & Humidity) - Pin D4 (GPIO2)
 * 2. MQ2 (Smoke/Gas Analog Sensor)
 * 3. MQ3 (Alcohol/Vapor Analog Sensor)
 *
 * Hardware limitation note:
 * ESP8266 has only ONE analog input pin (A0).
 * - Set USE_ADS1115 to 1 if you have an external ADS1115 I2C ADC module.
 *   ADS1115 SCL -> ESP8266 D1 (GPIO 5)
 *   ADS1115 SDA -> ESP8266 D2 (GPIO 4)
 *   MQ2 Analog Output -> ADS1115 Channel A0
 *   MQ3 Analog Output -> ADS1115 Channel A1
 *
 * - Set USE_ADS1115 to 0 if you are connecting MQ2 directly to A0.
 *   In this mode, MQ3 is simulated with random normal fluctuations
 *   to allow testing and pipeline training immediately.
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// ==========================================
// CONFIGURATION FLAGS
// ==========================================
#define USE_ADS1115 0 // Set to 1 if using ADS1115 I2C ADC module. Set to 0 for fallback mode (MQ2 on A0, MQ3 mocked)

#if USE_ADS1115
#include <Wire.h>
#include <Adafruit_ADS1X15.h>
Adafruit_ADS1115 ads;
#endif

// ==========================================
// SYSTEM PARAMETERS
// ==========================================
const unsigned long PUBLISH_INTERVAL_MS = 5000; // Publish every 5 seconds (non-blocking)

// WiFi Credentials
const char *ssid = "ComedKares-Students";
const char *password = "comedkares@12345";

// Mosquitto Broker Configuration
const char *mqtt_server = "192.168.0.233";
const uint16_t mqtt_port = 1883;
const char *mqtt_client_id = "ESP8266_Tunnel_Sensors";
const char *mqtt_pub_topic = "tunnel/sensors";

// DHT11 Pin & Sensor Definition
#define DHTPIN 2 // Pin D4 is GPIO2 on ESP8266 NodeMCU
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// WiFi & MQTT Clients
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastPublishTime = 0;

// Fallback / Last Known Good Readings (Prevent NaNs from breaking the pipeline)
float lastTemp = 22.0;
float lastHum = 55.0;

void setup_wifi()
{
  delay(10);
  Serial.println();
  Serial.print("Connecting to SSID: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());
  Serial.println();
  Serial.println("WiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect()
{
  // Loop until we are reconnected to MQTT Broker
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");

    // Attempt to connect
    if (client.connect(mqtt_client_id))
    {
      Serial.println(" connected!");
    }
    else
    {
      Serial.print(" failed, rc=");
      Serial.print(client.state());
      Serial.println(". Retrying in 5 seconds...");
      delay(5000); // Retry delay
    }
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.println("\n--- ESP8266 Tunnel Exhaust Sensor Initializing ---");

  // Initialize DHT sensor
  dht.begin();

  // Initialize I2C and ADS1115 if configured
#if USE_ADS1115
  Serial.println("Initializing ADS1115 I2C ADC...");
  Wire.begin(4, 5); // SDA on Pin D2 (GPIO4), SCL on Pin D1 (GPIO5)
  if (!ads.begin())
  {
    Serial.println("ERROR: ADS1115 not found! Check connections.");
  }
  else
  {
    Serial.println("ADS1115 detected and initialized successfully.");
  }
#else
  Serial.println("ADS1115 disabled. Using ESP8266 A0 pin for MQ2 (MQ3 will be simulated).");
#endif

  // Connect to WiFi
  setup_wifi();

  // Configure MQTT server and connection settings
  client.setServer(mqtt_server, mqtt_port);
}

void loop()
{
  // Ensure connection is active
  if (!client.connected())
  {
    reconnect();
  }

  // Handle PubSubClient internal state (keep-alives, input buffers, etc.)
  client.loop();

  unsigned long now = millis();
  if (now - lastPublishTime >= PUBLISH_INTERVAL_MS)
  {
    lastPublishTime = now;

    // 1. Read DHT11 Temperature and Humidity
    float humidity = dht.readHumidity();
    float temp = dht.readTemperature();

    // Check if reading failed and use last known good reading as fallback
    if (isnan(humidity) || isnan(temp))
    {
      Serial.println("WARNING: Failed to read from DHT11 sensor! Using fallback.");
      temp = lastTemp;
      humidity = lastHum;
    }
    else
    {
      lastTemp = temp;
      lastHum = humidity;
    }

    // 2. Read MQ2 and MQ3 Analog Sensors
    int mq2Raw = 0;
    int mq3Raw = 0;

#if USE_ADS1115
    // Read from ADS1115 channels A0 and A1
    // ADS1115 outputs 16-bit signed values (0-32767 for positive voltages).
    // The ML model pipeline is built on 10-bit range (0-1023) analog inputs.
    // We scale the reading to match standard 0-1023 ADC resolution:
    int16_t adsCh0 = ads.readADC_SingleEnded(0);
    int16_t adsCh1 = ads.readADC_SingleEnded(1);

    // Ensure we handle negative values (just in case of noise) and scale to 10-bit (0-1023)
    if (adsCh0 < 0)
      adsCh0 = 0;
    if (adsCh1 < 0)
      adsCh1 = 0;

    // Standard ADS1115 reading at default gain represents max voltage (typically ~6.144V)
    // Scale 16-bit range down to 10-bit range (Divide by 32 for rough mapping 32768->1024)
    mq2Raw = adsCh0 / 32;
    mq3Raw = adsCh1 / 32;

    // Bounds check
    if (mq2Raw > 1023)
      mq2Raw = 1023;
    if (mq3Raw > 1023)
      mq3Raw = 1023;
#else
    // Fallback Mode: Read physical A0 pin for MQ2_Raw
    mq2Raw = analogRead(A0);

    // Simulate MQ3_Raw (Ethanol/Vapor) value to test end-to-end integration.
    // Baseline normally floats between 80 and 100.
    // If MQ2 is elevated, we can simulate elevated MQ3 to match typical tunnel chemical conditions,
    // or just generate values within normal ranges.
    if (mq2Raw > 200)
    {
      mq3Raw = random(120, 250); // Simulate chemical vapor/smoke ratio
    }
    else
    {
      mq3Raw = random(80, 100); // Normal range
    }
#endif

    // Print values to Serial Monitor for troubleshooting
    Serial.println("\n=================================");
    Serial.print("Temperature : ");
    Serial.print(temp);
    Serial.println(" *C");
    Serial.print("Humidity    : ");
    Serial.print(humidity);
    Serial.println(" %");
    Serial.print("MQ2 Raw     : ");
    Serial.println(mq2Raw);
    Serial.print("MQ3 Raw     : ");
    Serial.println(mq3Raw);

    // 3. Assemble JSON Payload (formatted to match the ML pipeline columns)
    char payload[150];
    snprintf(payload, sizeof(payload),
             "{\"Temperature\":%.1f,\"Humidity\":%.1f,\"MQ2_Raw\":%d,\"MQ3_Raw\":%d}",
             temp, humidity, mq2Raw, mq3Raw);

    // 4. Publish to MQTT Broker
    Serial.print("Publishing payload: ");
    Serial.println(payload);

    if (client.publish(mqtt_pub_topic, payload))
    {
      Serial.println("MQTT Publish Success!");
    }
    else
    {
      Serial.println("MQTT Publish Failed!");
    }
  }
}
