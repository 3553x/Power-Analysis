import serial, time

BAUD_RATE = 2_000_000
DEBUG = 0
BS = 16
KEY = "c1e5ec7b1a30e0da98d34ff07030fe65"

class ArdSerial:

    def __init__ (self, dev="/dev/ttyACM1"):
        self.serial = serial.Serial(dev, BAUD_RATE)
        time.sleep(2) #Write is missed otherwise


    def encrypt(self, cleartext):
        assert len(cleartext) == BS

        if(DEBUG):
            while(True):
                line = self.serial.readline()
                print(line)

                if(line == b"NEED INPUT\r\n"):
                    break

        assert BS == self.serial.write(cleartext)

        if(DEBUG):
            print(self.serial.readline())
            rec_pt = self.serial.read(BS)
            print(rec_pt.hex())

        ct = self.serial.read(BS)
        
        return ct
