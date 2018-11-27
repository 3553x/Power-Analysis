#!/usr/bin/python3
import serial, sys

from Crypto.Cipher import AES

BAUD_RATE = 2_000_000
DEBUG = 1
BS = 16
KEY = "c1e5ec7b1a30e0da98d34ff07030fe65"

class ArdSerial:

    def __init__ (self, dev="/dev/ttyACM0"):
        self.serial = serial.Serial(dev, BAUD_RATE)


    def encrypt(self, cleartext):
        print(cleartext) 
        assert len(cleartext) == BS

        if(DEBUG):
            while(True):
                line = self.serial.readline()
                print(line)

                if(line == b"NEED INPUT\r\n"):
                    break

        self.serial.write(cleartext)
        self.serial.flush()

        if(DEBUG):
            print(self.serial.readline())
            rec_pt = self.serial.read(BS)
            print(rec_pt.hex())


        ct = self.serial.read(BS)
        
        if(DEBUG):
            print(self.serial.readline())
        return ct



if(__name__ == "__main__"):
    inter = ArdSerial()
    ct = inter.encrypt(bytes([0]*16))

    cipher = AES.new(bytes(bytearray.fromhex(KEY)), AES.MODE_ECB)
    ct2 = cipher.encrypt(bytes([0]*16))

    print(ct.hex())
    print(ct2.hex())
    

