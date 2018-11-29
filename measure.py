#!/usr/bin/python3
from scope_inter import Scope
from arduino_inter import ArdSerial, KEY, BS
from converter.tektronix_converter import convert

from Crypto.Cipher import AES
from os import urandom

def init_scope(scope):
  scope.acquire_stopafter("RUNST")
  scope.data_encoding("RIB")
  scope.data_width("2")
  scope.data_start("1")
  scope.data_stop("10000")
  scope.acquire_state("RUN")
  while("ARMED" in scope.trigger_state()):
    pass

def take_measurement(scope, arduino, cleartext):
  ciphertext = arduino.encrypt(cleartext)
  while(scope.busy() != ":BUSY 0"):
    pass
    
  scope.data_source("MATH")
  csv = convert(scope.waveform())

  return (ciphertext, csv)


def gather_data(n):
  crypt = AES.new(bytes.fromhex(KEY), AES.MODE_ECB)
  
  scope = Scope()
  init_scope(scope)

  arduino = ArdSerial()

  capt_f = open("captures", 'a')
  pt_f = open("plaintext", "ab")
  ct_f = open("ciphertext", "ab")


  for x in range(n):
    plaintext = urandom(BS)
    (ciphertext, csv) = take_measurement(scope, arduino, plaintext)
    assert ciphertext == crypt.encrypt(plaintext)
    
    capt_f.write(csv)
    pt_f.write(plaintext)
    ct_f.write(ciphertext)
 


if(__name__ == "__main__"):
  gather_data(100)
