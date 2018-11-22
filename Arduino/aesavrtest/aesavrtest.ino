#include <aes-avr.h>

#define KEY_MATERIAL {0xc1, 0xe5, 0xec, 0x7b, 0x1a, 0x30, 0xe0, 0xda, 0x98, 0xd3, 0x4f, 0xf0, 0x70, 0x30, 0xfe, 0x65}

char expanded_key[176];

void setup()
{
  Serial.begin(9600);
  struct data keyMaterial = {KEY_MATERIAL};
  expand_key(keyMaterial, expanded_key);
}

void loop()
{
 Serial.println("Start");
 struct data pt;
 pt = {0};
  //for(int i = 0; i < 16; i++)
 // Serial.print(String(pt.data[i], HEX));
 // Serial.println();
 struct data ct;
  for(int i = 0; i < 16; i++)
  Serial.print(String(ct.data[i], HEX));
  Serial.println();
 ct = encrypt_data(pt, expanded_key); 
 //Serial.write(ct.data, 16, HEX);
 for(int i = 0; i < 16; i++)
  Serial.print(String(ct.data[i], HEX));
  Serial.println();
}
  
