#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

#define TRIG 5
#define ECHO 18
#define GREEN 13
#define YELLOW 12
#define RED 14
#define BUZZER 19
#define SDA_PIN 21 // OLED Data
#define SCL_PIN 22 // OLED Clock

int binHeight = 30; 

void setup() {
  Serial.begin(115200);
  
  // OLED Setup
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  display.clearDisplay();
  
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(RED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
}

void loop() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  long duration = pulseIn(ECHO, HIGH);
  float distance = duration * 0.034 / 2;

  int fillLevel = ((binHeight - distance) / (float)binHeight) * 100;
  fillLevel = constrain(fillLevel, 0, 100);

  // Control LEDs and Buzzer
  digitalWrite(GREEN,  (fillLevel <= 40) ? HIGH : LOW);
  digitalWrite(YELLOW, (fillLevel > 40 && fillLevel <= 80) ? HIGH : LOW);
  digitalWrite(RED,    (fillLevel > 80) ? HIGH : LOW);
  
  if(fillLevel > 80) {
    tone(BUZZER, 1000);
  } else {
    noTone(BUZZER);
  }

  // --- OLED VISUAL BIN ---
  display.clearDisplay();
  
  // Draw Bin Outline
  display.drawRect(80, 10, 30, 50, WHITE); // Main body
  display.fillRect(85, 5, 20, 5, WHITE);  // Lid handle
  
  // Draw Fill Level (The "Trash")
  int fillBarHeight = map(fillLevel, 0, 100, 0, 46);
  display.fillRect(82, 58 - fillBarHeight, 26, fillBarHeight, WHITE);
  
  // Text Data
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  display.print("WASTE LEVEL:");
  
  display.setTextSize(2);
  display.setCursor(0, 30);
  display.print(fillLevel);
  display.print("%");
  
  display.setTextSize(1);
  display.setCursor(0, 55);
  display.print(fillLevel > 80 ? "STATUS: FULL" : "STATUS: OK");

  display.display();
  
  String status = "";
  if (fillLevel > 80) {
    status = "FULL";
  } else if (fillLevel > 40) {
    status = "MEDIUM";
  } else {
    status = "LOW";
  }

  // --- Enhanced Serial Output ---
  Serial.println("===============================");
  Serial.print("Status: ");
  Serial.println(status);
  
  Serial.print("Fill Level: [");
  // This creates a visual loading bar in the terminal: [######    ]
  int barWidth = 20;
  int pos = (fillLevel * barWidth) / 100;
  for (int i = 0; i < barWidth; i++) {
    if (i < pos) Serial.print("#");
    else Serial.print(" ");
  }
  Serial.print("] ");
  Serial.print(fillLevel);
  Serial.println("%");

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  Serial.println("===============================");

  delay(500);
}