#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9
#define SS_PIN 10
#define PIR_PIN 2
#define TRIG_PIN 5
#define ECHO_PIN 6
#define LDR_PIN A0

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  pinMode(PIR_PIN, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  // PIR con filtro de ruido
  int movimiento = 0;
  for(int i=0; i<10; i++) {
    movimiento += digitalRead(PIR_PIN);
    delay(50);
  }
  movimiento = (movimiento > 5) ? 1 : 0;
  
  // Ultrasónico
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  int distancia = pulseIn(ECHO_PIN, HIGH) * 0.034 / 2;
  
  // LDR calibrado
  int raw_ldr = analogRead(LDR_PIN);
  int luz = map(raw_ldr, 200, 800, 100, 0); // Ajusta estos valores
  
  // RFID
  String tarjeta = "N/A";
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      tarjeta += String(mfrc522.uid.uidByte[i], HEX);
    }
    mfrc522.PICC_HaltA();
  }
  
  // Enviar datos
  Serial.print("RFID:" + tarjeta + 
               ",PIR:" + String(movimiento) + 
               ",US:" + String(distancia) + 
               ",LDR:" + String(luz));
  Serial.println();
  
  delay(300);
}
