
#include "Adafruit_Thermal.h"
#include "SoftwareSerial.h"

#include "amperka_logo.h"

constexpr uint8_t TX_PIN = 6;
constexpr uint8_t RX_PIN = 5;

SoftwareSerial mySerial(RX_PIN, TX_PIN);
Adafruit_Thermal printer(&mySerial);

void setup() {
  mySerial.begin(9600);
  printer.begin();
  printer.printBitmap(384, 384, amperka_logo);
  printer.feed(10);
}

void loop() {
}
