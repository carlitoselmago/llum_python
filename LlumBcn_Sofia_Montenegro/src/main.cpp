// Basic demo for accelerometer readings from Adafruit MPU6050

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <ArduinoOSCWiFi.h>
#include <Wire.h>
#include "Adafruit_MAX1704X.h"
#include "Adafruit_LC709203F.h"

#define readId 7   //ID
#define resolution 0.0005//0.05//0.0005

#if readId==0
 const char *board = "/board0";
#elif readId==1
 const char *board = "/board1";
#elif readId==2
 const char *board = "/board2";
#elif readId==3
 const char *board = "/board3";
#elif readId==4
 const char *board = "/board4";
#elif readId==5
 const char *board = "/board5";
#elif readId==6
 const char *board = "/board6";
#elif readId==7
 const char *board = "/board7";
#elif readId==8
 const char *board = "/board8";
#elif readId==9
 const char *board = "/board9";
#elif readId==10
 const char *board = "/board10";
#elif readId==11
 const char *board = "/board11";
#elif readId==12
 const char *board = "/board12";
#elif readId==13
 const char *board = "/board13";
#endif

Adafruit_MPU6050 mpu;
Adafruit_MAX17048 maxlipo;
Adafruit_LC709203F lc;

// MAX17048 i2c address
bool addr0x36 = true;

/*
//Wifi configuration
const char *ssid = "HANGAR_lab";
const char *password = "mordorlab";

IPAddress ip(192, 168, 30, 200 + readId);
IPAddress gateway(192, 168, 30, 1);
IPAddress subnet(255, 255, 255, 0);

// for ArduinoOSC
const char* host_ip = "192.168.30.255";
*/
/*
//Wifi configuration
const char *ssid = "( o )( o )";
const char *password = "todojuntoyenminusculas";

IPAddress ip(192, 168, 1, 200 + readId);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
const char* host_ip = "192.168.1.139";
*/
/*
//Wifi configuration
const char *ssid = "HANGAR_residents";
const char *password = "residentsQjFXlm4X";

IPAddress ip(172, 25, 0, 200 + readId);
IPAddress gateway(172, 25, 0, 1);
IPAddress subnet(255, 255, 248, 0);
const char* host_ip = "172.25.0.250";
*/
//Wifi configuration
const char *ssid = "MANGO";
const char *password = "remotamente";

IPAddress ip(192, 168, 4, 200 + readId);
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 255, 0);
const char* host_ip = "192.168.4.100";

void setup(void) {
  Serial.begin(115200);
  //while (!Serial)
    //delay(5000); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println(readId);
        if (WiFi.config(ip, gateway, subnet) == false) {
          Serial.println("Configuration failed.");
        }
    WiFi.begin(ssid, password);
    int retry = 0;
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      retry++;
      if(retry==10)
        {
          Serial.print("Restarting...\n\n");
          ESP.restart();
        }
      Serial.print("Connecting...\n\n");
    }

  Serial.println("Adafruit MPU6050 test!");

  //Battery level
  // if no max17048..
  if (!maxlipo.begin()) {
    Serial.println(F("Couldnt find Adafruit MAX17048, looking for LC709203F.."));
    // if no lc709203f..
    if (!lc.begin()) {
      Serial.println(F("Couldnt find Adafruit MAX17048 or LC709203F."));
      while (1) delay(10);
    }
    // found lc709203f!
    else {
      addr0x36 = false;
      Serial.println(F("Found LC709203F"));
      Serial.print("Version: 0x"); Serial.println(lc.getICversion(), HEX);
      lc.setThermistorB(3950);
      Serial.print("Thermistor B = "); Serial.println(lc.getThermistorB());
      lc.setPackSize(LC709203F_APA_500MAH);
      lc.setAlarmVoltage(3.8);
    }
  // found max17048!
  }
  else {
    addr0x36 = true;
    Serial.print(F("Found MAX17048"));
    Serial.print(F(" with Chip ID: 0x")); 
    Serial.println(maxlipo.getChipID(), HEX);
  }

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
      Serial.println("Failed to find MPU6050 chip");
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

  Serial.println("");
  delay(100);

  // subscribe osc messages
  int recv_port = 55555;
  OscWiFi.subscribe(recv_port, "/curtain/start",
          [&](const int& dir_osc, const int& val) {
              Serial.print("/curtain/start ");
              Serial.print(dir_osc);
              Serial.println();
          });
}

float bat_level = 10.0;

void lc709203f() {
  /*Serial.print("Batt_Voltage:");
  Serial.print(lc.cellVoltage(), 3);
  Serial.print("\t");
  Serial.print("Batt_Percent:");
  Serial.print(lc.cellPercent(), 1);
  Serial.print("\t");
  Serial.print("Batt_Temp:");
  Serial.println(lc.getCellTemperature(), 1);*/
  bat_level = lc.cellPercent();
}

void max17048() {
  /*Serial.print(F("Batt Voltage: ")); Serial.print(maxlipo.cellVoltage(), 3); Serial.println(" V");
  Serial.print(F("Batt Percent: ")); Serial.print(maxlipo.cellPercent(), 1); Serial.println(" %");
  Serial.println();*/
  bat_level = maxlipo.cellPercent();
}

float axis_x_ant, axis_y_ant,axis_z_ant, bat_level_ant;

void loop() {

  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  // if you have the max17048..
  if (addr0x36 == true) {
    max17048();
  }
  // if you have the lc709203f..
  else {
    lc709203f();
  }

  OscWiFi.update();

  if((abs(axis_x_ant-a.acceleration.x)>=resolution)||(abs(axis_y_ant-a.acceleration.y)>=resolution)||(abs(axis_z_ant-a.acceleration.z)>=resolution)||(abs(bat_level_ant-bat_level)>=0.1))
    {
      /* Print out the values */
      OscWiFi.send(host_ip, 54321, board, 10*a.acceleration.x, 10*a.acceleration.y, 10*a.acceleration.z, bat_level);
      axis_x_ant = a.acceleration.x;
      axis_y_ant = a.acceleration.y;
      axis_z_ant = a.acceleration.z;
      bat_level_ant = bat_level;
      //OscWiFi.send("192.168.30.255", 54321, board, 10*g.gyro.x, 10*g.gyro.y, 10*g.gyro.z);
    }   
  

  delay(50);
}

