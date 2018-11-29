#!/usr/bin/python3
from scope_inter import Scope
from arduino_inter import ArdSerial, KEY, BS
from converter.tektronix_converter import convert

from Crypto.Cipher import AES
from os import urandom
from sqlalchemy import create_engine
from threading import Thread

import pandas
import io

def init_scope(scope):
  scope.acquire_stopafter("SEQ")
  scope.data_encoding("RIB")
  scope.data_width("2")
  scope.data_start("1")
  scope.data_stop("10000")
  scope.acquire_state("OFF")

def take_measurement(scope, arduino, cleartext):
  scope.acquire_state("RUN")
  while(scope.trigger_state() == "ARMED"):
    pass
  ciphertext = arduino.encrypt(cleartext)
  while(scope.busy() == "1"):
    pass
    
  scope.data_source("CH1")
  csv_ch1 = convert(scope.waveform())
  scope.data_source("CH2")
  csv_ch2 = convert(scope.waveform())
  scope.data_source("CH3")
  csv_ch3 = convert(scope.waveform())

  return (ciphertext, csv_ch1, csv_ch2, csv_ch3)


def gather_data(n):
  crypt = AES.new(bytes.fromhex(KEY), AES.MODE_ECB)
  
  scope = Scope()
  init_scope(scope)

  arduino = ArdSerial()

  engine = create_engine("sqlite:///measurements.db")
  con = engine.connect()
  con.execute("CREATE TABLE IF NOT EXISTS data (ciphertext TEXT NOT NULL, plaintext TEXT NOT NULL);")

  for x in range(n):
    plaintext = urandom(BS)
    (ciphertext, csv_ch1, csv_ch2, csv_ch3) = take_measurement(scope, arduino, plaintext)
    assert ciphertext == crypt.encrypt(plaintext)
    df_1 = pandas.read_csv(io.StringIO(csv_ch1), names=["S", "V"])
    df_2 = pandas.read_csv(io.StringIO(csv_ch2), names=["S", "V"])
    df_3 = pandas.read_csv(io.StringIO(csv_ch3), names=["S", "V"])
    df_1.to_sql('samples_ch1', engine, if_exists='append', index=False)
    df_2.to_sql('samples_ch2', engine, if_exists='append', index=False)
    df_3.to_sql('samples_ch3', engine, if_exists='append', index=False)

    con.execute("INSERT INTO data VALUES ('%s', '%s')" % (ciphertext.hex(), plaintext.hex()))

  con.close()

if(__name__ == "__main__"):
  gather_data(5)
