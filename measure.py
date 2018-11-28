#!/usr/bin/python3
from scope_inter import Scope
from arduino_inter import ArdSerial, KEY, BS
from converter.tektronix_converter import convert

from Crypto.Cipher import AES
from os import urandom
from sqlalchemy import create_engine

import pandas

def init_scope(scope):
  scope.acquire_stopafter("SEQ")
  scope.data_encoding("RIB")
  scope.data_width("2")
  scope.data_start("1")
  scope.data_stop("10000")

def take_measurement(scope, arduino, cleartext)
  assert scope.busy() == "0"
  scope.acquire_state("RUN")
  assert scope.busy() == "1"
  ciphertext = arduino.encrypt(cleartext)
  assert scope.busy() == "0"
  
  scope.data_source("CH1")
  csv_ch1 = convert(scope.waveform())
  scope.data_source("CH2")
  csv_ch2 = convert(scope.waveform())

  return (ciphertext, csv_ch1, csv_ch2)


def gather_data(n):
  crypt = AES.new(bytearray.fromhex(KEY), AES.MODE_ECB)
  
  scope = Scope()
  init_scope(scope)

  arduino = ArdSerial()

  engine = create_engine("sqlite:///measurements.db")
  con = engine.connect()
  con.execute("CREATE TABLE IF NOT EXISTS data (ciphertext TEXT NOT NULL, plaintext TEXT NOT NULL);")

  for x in xrange(n):
    plaintext = urandom(BS)
    (ciphertext, csv_ch1, csv_ch2) = take_measurement(scope, arduino, plaintext)
    assert ciphertext == crypt.encrypt(plaintext)
    df_1 = pandas.read_csv(csv_ch1)
    df_2 = pandas.read_csv(csv_ch2)
    df_1.to_sql('samples_ch1', engine, if_exists='append')
    df_2.to_sql('samples_ch2', engine, if_exists='append')

    con.execute("INSERT INTO data VALUES (%s, %s)" % (ciphertext.hex(), plaintext.hex()))

  con.close()
  engine.close()

if(__name__ == "__main__"):
  gather_data(1000)
