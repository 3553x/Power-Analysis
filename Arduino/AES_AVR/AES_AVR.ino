#include <aes-avr.h>

//#define DEBUG
#define BS 16
#define TRIGGER_PIN 2
#define KEY_MATERIAL {0xc1, 0xe5, 0xec, 0x7b, 0x1a, 0x30, 0xe0, 0xda, 0x98, 0xd3, 0x4f, 0xf0, 0x70, 0x30, 0xfe, 0x65}

char expanded_key[176];

void setup()
{
  struct data key_material = {KEY_MATERIAL};
  expand_key(key_material, expanded_key);
  
  pinMode(TRIGGER_PIN, OUTPUT);
  Serial.begin(2000000);
}

void loop()
{
  struct data pt;
  struct data ct;

#ifdef DEBUG
  Serial.println("NEED INPUT");
#endif

  //while(!Serial.available())
  //{
  //  asm("NOP"); 
  //}
  
  //int result_read = Serial.readBytes(pt.data, BS);
  
#ifdef DEBUG
  Serial.print("GOT: ");
  Serial.println(result_read);
  Serial.write(pt.data, sizeof(pt.data));
#endif
  
  digitalWrite(TRIGGER_PIN, HIGH);
  ct = encrypt_data(pt, expanded_key);
  digitalWrite(TRIGGER_PIN, LOW);
  Serial.write(ct.data, sizeof(ct.data));  
}


