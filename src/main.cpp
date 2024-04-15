#include <M5Core2.h>

void setup() {
    M5.begin(true, false, true); // set the first parameter to true to enable the lcd screen
    //Serial2.begin(9600, SERIAL_8N1, 13, 14);
    Serial.begin(115200);
    M5.IMU.Init();
    M5.Lcd.println("ON");
}

void loop() {
    M5.update();
    float accX, accY, accZ;
    M5.IMU.getAccelData(&accX, &accY, &accZ);
    char buf[64];
    sprintf(buf, "%.4f,%.4f,%.4f\r\n", accX, accY, accZ);
    Serial.print(buf);
    delay(16);
}