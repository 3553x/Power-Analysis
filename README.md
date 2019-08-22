# Power Analysis
This is a past university project of mine.
For more details, see my blogpost.

## Contents

### Arduino
Firmware running on the arduino. 
libraries contains a reference implementation of AES in C and a very efficient assembly implementation with C bindings added on top.
AES contains a sketch that uses the C implementation while AES_AVR uses the ASM implementation and is far more efficient.

### arduino_inter.py
A small python module that can be used to encrypt data with the Arduino firmware.

### generate_rks.c
Takes a hardcoded initial key for AES128, expands it into all the roundkeys and dumps it to a file.

### measure.py
Coordinates between the oscilloscope and the Arduino to encrypt data and capture the power traces.

### scope_inter.py
A small python module that interfaces with the oscilloscope and exposes a tiny python library.

### process_data.py
Perform the attack on captured data.

### recover_initial_key.py
A short script that takes the final roundkey and returns the initial AES128 key.
