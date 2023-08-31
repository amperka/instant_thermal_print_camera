
#include "Adafruit_Thermal.h"
#include "SoftwareSerial.h"

#include "amperka_logo.h"

constexpr uint8_t TX_PIN = 6;
constexpr uint8_t RX_PIN = 5;
constexpr uint8_t DTR_PIN = 2;

SoftwareSerial mySerial(RX_PIN, TX_PIN);
Adafruit_Thermal printer(&mySerial, DTR_PIN);

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  printer.begin();
  printer.feed(10);
  printer.printBitmapMy(384, 384, amperka_logo);
  printer.printBitmapMy(384, 384, amperka_logo);
  printer.printBitmapMy(384, 384, amperka_logo);
  printer.feed(10);
}

void loop() {
}
