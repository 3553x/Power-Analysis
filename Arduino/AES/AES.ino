#include <rijndael-api-ref.h>

#define DEBUG
#define BS 16
#define TRIGGER_PIN 2
#define KEY_MATERIAL "c1e5ec7b1a30e0da98d34ff07030fe65"



keyInstance key;
cipherInstance cipher;

void setup()
{
  char key_material[] = KEY_MATERIAL;
  
  key.blockLen = 128;
  cipher.blockLen = 128;
  
  static_assert(sizeof(key_material) * 8 / 2 == 128 + 4
             || sizeof(key_material) * 8 / 2 == 192 + 4
             || sizeof(key_material) * 8 / 2 == 256 + 4,
                   "INVALID KEY LENGTH");
  
  int result_key = makeKey(&key, DIR_ENCRYPT, sizeof(key_material) * 8 / 2 - 4, key_material);
  int result_init = cipherInit(&cipher, MODE_ECB, (char *)0);
  
  pinMode(TRIGGER_PIN, OUTPUT);
  
  Serial.begin(2000000);
  
#ifdef DEBUG
  Serial.print("Key result: ");
  Serial.println(result_key);
  
  Serial.print("Init result: ");
  Serial.println(result_init);
#endif

}

void loop()
{
  char input[BS];
  char output[BS];

#ifdef DEBUG
  Serial.println("NEED INPUT");
#endif

  while(!Serial.available())
  {
    asm("NOP"); 
  }
  
  int result_read = Serial.readBytes(input, BS);
  
#ifdef DEBUG
  Serial.print("GOT: ");
  Serial.println(result_read);
  Serial.write((uint8_t *)input, sizeof(input));
#endif
  
  digitalWrite(TRIGGER_PIN, HIGH);
  int result_enc  = blockEncrypt(&cipher, &key, (BYTE *)input, sizeof(input) * 8, (BYTE *)output);
  digitalWrite(TRIGGER_PIN, LOW);
  Serial.write((uint8_t *)output, sizeof(output));
  
#ifdef DEBUG
  Serial.print("Enc result: ");
  Serial.println(result_enc);
#endif
  
}


