#include "Rijndael/rijndael-api-ref.h"
#include <stdio.h>

int
main(int argc, char **argv)
{
  char *rawkey = "c1e5ec7b1a30e0da98d34ff07030fe65";

  keyInstance key;
  key.blockLen = 128;

  if(makeKey(&key, DIR_ENCRYPT, 128, rawkey) < 0)
  {
    puts("ERROR");
    return -1;
  }

  FILE *output = fopen("roundkeys", "w");
  for(int x = 0; x < 11; x++)
    for(int y = 0; y < 4; y++)
      for(int z = 0; z < 4; z++)
      {
        fwrite(key.keySched[x][z] + y, 1, 1, output);
      }
    fclose(output);

    return 0;

}
