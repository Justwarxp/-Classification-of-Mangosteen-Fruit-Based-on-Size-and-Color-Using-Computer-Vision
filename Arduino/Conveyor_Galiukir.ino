#include <ESP32Servo.h>

int relay = 2;
Servo servo;
int port_servo = 15; 
Servo servo_2;
int port_servo_2 = 23; 
Servo servo_3;
int port_servo_3 = 22;
Servo servo_4;
int port_servo_4 = 21;
Servo servo_5;
int port_servo_5 = 18;
int port_buzzer = 5;

String baca_serial() {
  String s;
  while (Serial.available() > 0) {
    delay(10);
    char c = Serial.read();
    s += c;
  }
  delay(100);
  return s;
}

void relay_on()
{
digitalWrite(relay ,HIGH);
}
void relay_off()
{
digitalWrite(relay ,LOW);
}
void posisi_servo(int posisi)
{
servo.write(posisi);
}
void posisi_servo_2(int posisi)
{
servo_2.write(posisi);
}
void posisi_servo_3(int posisi)
{
servo_3.write(posisi);
}
void posisi_servo_4(int posisi)
{
servo_4.write(posisi);
}
void posisi_servo_5(int posisi)
{
servo_5.write(posisi);
}
void buzzer_on()
{
  digitalWrite(port_buzzer,HIGH);
}
void buzzer_off()
{
  digitalWrite(port_buzzer,LOW);
}
void buzzer_bip()
{
  digitalWrite(port_buzzer,HIGH);
  delay(500);
  digitalWrite(port_buzzer,LOW);
}
void buzzer_bipbip()
{
  digitalWrite(port_buzzer,HIGH);
  delay(500);
  digitalWrite(port_buzzer,LOW);
  delay(500);
  digitalWrite(port_buzzer,HIGH);
  delay(500);
  digitalWrite(port_buzzer,LOW);
  delay(500);
}



void setup()
{
Serial.begin(9600);
pinMode(relay, OUTPUT);


relay_off();
servo.attach(port_servo);
posisi_servo(0);
servo_2.attach(port_servo_2);
posisi_servo_2(0);
servo_3.attach(port_servo_3);
posisi_servo_3(0);
servo_4.attach(port_servo_4);
posisi_servo_4(0);
servo_5.attach(port_servo_5);
posisi_servo_5(0);
pinMode(port_buzzer, OUTPUT);
buzzer_bipbip();

Serial.println("Ready");

}
void loop(){
int kode = 0;
String text_serial = baca_serial();
if (text_serial.length() > 0) {
   Serial.println (text_serial);
   delay(1000);
   kode = text_serial.toInt();

    if (kode >= 1 && kode <= 6) { 
    buzzer_on();
    delay(1000);
    buzzer_off();
    delay(1000);
    
    
    }

  } 


if (kode == 1)
{
posisi_servo(0);
delay(1000);
posisi_servo(122);
delay(1000);
relay_on();
delay(10000);
posisi_servo(0);
delay(1000);



}

if (kode == 2)
{
posisi_servo_2(0);
delay(1000);
posisi_servo_2(126);
delay(1000);
relay_on();
delay(15000);
posisi_servo_2(0);
delay(1000);


}

if (kode == 3)
{
posisi_servo_3(0);
delay(1000);
posisi_servo_3(121);
delay(1000);
relay_on();
delay(18000);
posisi_servo_3(0);
delay(1000);


}


if (kode == 4)
{
posisi_servo_4(0);
delay(1000);
posisi_servo_4(123);
delay(1000);
relay_on();
delay(19000);
posisi_servo_4(0);
delay(1000);


}


if (kode == 5)
{
posisi_servo_5(0);
delay(3000);
posisi_servo_5(110);
relay_on();
delay(19000);
posisi_servo_5(0);
delay(1000);


}

if (kode == 6)
{
relay_on();
delay(19000);
}


relay_off();


}
