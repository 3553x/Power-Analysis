#!/usr/bin/python3
from scope_inter import Scope
from arduino_inter import ArdSerial, KEY, BS
from converter.tektronix_converter import convert

from Crypto.Cipher import AES
from os import urandom
import time, signal

def init_scope(scope):
  scope.acquire_stopafter("SEQ")
  scope.data_source("MATH")
  scope.data_encoding("RIB")
  scope.data_width("2")
  scope.data_start("1")
  scope.data_stop("10000")

def take_measurement(scope, arduino, cleartext):
  scope.acquire_state("RUN")
  while("READY" not in scope.trigger_state()):
    pass

  ciphertext = arduino.encrypt(cleartext)

  while("SAV" not in scope.trigger_state()):
    pass

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
     
    s = signal.signal(signal.SIGINT, signal.SIG_IGN)
    capt_f.write(csv)
    capt_f.flush()
    pt_f.write(plaintext)
    pt_f.flush()
    ct_f.write(ciphertext)
    ct_f.flush()
    signal.signal(signal.SIGINT, s)

  capt_f.close()
  pt_f.close()
  ct_f.close()
 


if(__name__ == "__main__"):
  gather_data(10_000)
