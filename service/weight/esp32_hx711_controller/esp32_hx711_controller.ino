#include "HX711.h"  // https://github.com/RobTillaart/HX711 (0.5.2)
#include <Wire.h>

// I2C slave address
const int SLAVE_ADDRESS = 0x50;

HX711 scale0;
HX711 scale1;
HX711 scale2;
HX711 scale3;
HX711 scales[] = {scale0, scale1, scale2, scale3};

//  adjust pins if needed
uint8_t dataPin[] = {1, 2, 3, 4};
uint8_t clockPin = 0;

const int ARRAY_SIZE = 4;
float f[ARRAY_SIZE] = {0, 0, 0, 0};
int requestedIndex = -1; // 요청받은 인덱스를 저장할 변수


void setup()
{
  // Initialize I2C as slave
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
  


  Serial.begin(115200);
  //  Serial.println(__FILE__);
  //  Serial.print("HX711_LIB_VERSION: ");
  //  Serial.println(HX711_LIB_VERSION);
  //  Serial.println();

  for(int i=0; i<4; i++) {
    scales[i].begin(dataPin[i], clockPin);
  
    //  TODO find a nice solution for this calibration..
    //  load cell factor 20 KG
    //  scale.set_scale(127.15);
    //  load cell factor 5 KG
    scales[i].set_scale(100);       // TODO you need to calibrate this yourself.
    //  reset the scale to zero = 0
    scales[i].tare();

  }
}


void loop()
{
  //  continuous scale 4x per second
  for(int i=0; i<4; i++) {
    f[i] = scales[i].get_units(5);
    // Serial.print(f[i]);
    // Serial.print("\t");
  }
  // Serial.println();
  delay(250/4);
}

void receiveEvent(int howMany) {
  if (Wire.available() > 0) {
    requestedIndex = Wire.read(); // 요청받은 인덱스를 저장
    Serial.print("Received index: ");
    Serial.println(requestedIndex);
  }
}

void requestEvent() {
  if (requestedIndex >= 0 && requestedIndex < ARRAY_SIZE) {
    float value = f[requestedIndex];
    byte* bytes = (byte*)&value;
    Wire.write(bytes, sizeof(value)); // 직접 응답 전송
    requestedIndex = -1; // 다음 요청을 위해 초기화
  } else {
    Serial.println("Invalid index");
  }
}
