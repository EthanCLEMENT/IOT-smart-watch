// include the arduino
#include "U8glib.h"
#include <SoftwareSerial.h>

SoftwareSerial BLEserial(2, 3);

U8GLIB_SH1106_128X64 u8g(U8G_I2C_OPT_NONE);

// variables
int h2 = 0;
int h = 0;
int m2 = 0;
int m = 0;
int c = 0;
int timeinit=0;
int Signal;
int bpm = 0;
int bpmcount = 0;

String bpmstate = "on";

// updates time variables
unsigned long previoustimetimer = millis();
unsigned long previoustimeble = millis();
unsigned long previoustimebpm = millis();

// delays variables 
long timerdelay = 60000;
long bledelay = 3000;
long bpmdelay = 20;

// initiates the BLE
void setup() {
  pinMode(4,OUTPUT);
  pinMode(0,INPUT);
  digitalWrite(4,HIGH);
  BLEserial.begin(9600);
  Serial.begin(38400);
}

// displays info on the screen 
void draw2() {
  u8g.setFont(u8g_font_fur14); // initiates font
  u8g.setPrintPos(0, 25); // initiates text position 
  u8g.print("NextepWatch"); 
  u8g.setFont(u8g_font_5x8); // initiates font 
  u8g.setPrintPos(0,60); // print text position
  u8g.print("Waiting for BLE init...");
}

// displays the time
void draw() {
  u8g.setFont(u8g_font_fur35n);
  u8g.setPrintPos(5, 38);
  u8g.print(h2);u8g.print(h);u8g.print(":");u8g.print(m2);u8g.print(m);
}

// initiates watch tabs
void screen(){
  u8g.firstPage();
  if(timeinit != 0){
    do {draw();} while (u8g.nextPage() );
  }
  else{
    do {draw2();} while (u8g.nextPage() );
  }
}

// initiates the bpm 
void bpmread(){
  Signal = analogRead(0);
  if(Signal > 513){
    bpmcount += 1;
  } 
}

// bpm calc
void bpmcalc(){
  bpm = bpmcount * 4;
  bpmcount = 0;
}

// time controller
void timer(){
  m+=1;
  if (m > 9){
    m2 += 1;
    m = 0;
  }
  if (m2 > 5){
    m2 = 0;
    h += 1;
  }
  if (h > 9){
    h2 += 1;
    h = 0;
  }
  if (h2 == 2 and h == 4){
    h2 = 0;
    h = 0;
  }
}

// asks the user for the hours, the minutes, and the seconds 
void bletext(){
  if(BLEserial.available()>0){
    if (timeinit == 0){
      h = BLEserial.readStringUntil('h').toInt();
      m = BLEserial.readString().toInt();
      if (m > 9){
        m2 = m/10;
        m = m%10;
      }
      if (m2 > 5){
        m2 = 0;
        h += 1;
      }
      if (h > 9){
        h2 = h/10;
        h = h%10;
      }
      if (h2 == 2 and h == 4){
        h2 = 0;
        h = 0;
      }
      timeinit += 1;
      screen();
    }    
    if (timeinit > 0){
      String text = BLEserial.readString();    
      if(text == "bpmoff"){
        digitalWrite(4,LOW);
        bpmstate = "off";
      }
      if(text == "bpmon"){
        digitalWrite(4,HIGH);
        bpmstate = "on";
      }
    }
  }
}

// main loop
void loop() {
  unsigned long currentTime = millis();
  if ((currentTime- previoustimebpm > bpmdelay) && (bpmstate == "on")){
    previoustimebpm = currentTime;
    bpmread();
  }
  
  if (currentTime - previoustimetimer > timerdelay){
    previoustimetimer = currentTime;
    timer();
  }
  
  if (currentTime - previoustimeble > bledelay){
    previoustimeble = currentTime;
    bletext();
    screen();
    c += 1;
    if (c == 5){
      c = 0;
      bpmcalc();
    }
  } 
}
