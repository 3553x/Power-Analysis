import vxi11

IP = "10.0.0.1"
MAX_READ = 56608 #determined with trial and error

class Scope:
  
  def __init__(self, addr=IP):
    self.instr = vxi11.Instrument(addr)

  def write(self, message):
    self.instr.write(message)

  def write_raw(self, data):
    self.instr.write_raw(data)

  def ask(self, message):
    return self.instr.ask(message, MAX_READ)

  def ask_raw(self, data):
    return self.instr.ask_raw(data, MAX_READ)

  #0 = not busy
  #1 = busy
  def busy(self):
    return self.ask("BUSY?")
  
  #AUTO = triggers without trigger
  #ARMED = acquiring pretrigger info, ignores triggers
  #READY = ARMED passed, ready for trigger
  #SAVe = acquisition stopped or all channels off
  #TRIGger = trigger seen, acquiring posttriger info
  def trigger_state(self):
    return self.ask("TRIG:STATE?")
 
  #beep
  def bell(self):
    self.write("BEL")

  #arg:
  #OFF, STOP, 0 = stop acquisition
  #ON, NR != 0 = start of resume
  #RUN = restart
  #return:
  #0 = not running
  #1 = running
  def acquire_state(self, arg=None):
    if(arg):
      self.write("ACQ:STATE %s" % arg)
    else:
      return self.ask("ACQ:STATE?")

  #RUNSTop = determined by run/stop
  #SEQuence = single seq
  def acquire_stopafter(self, arg):
    self.write("ACQ:STOPA %s" % arg)

  #CH1, CH2, CH3, CH4, MATH, REF1, REF2, REF3, REF4
  def data_source(self, arg):
    self.write("DAT:SOU %s" % arg)

  #ASCIi, RIBinary, RPBinary, SRIbinary, SRPbinary
  def data_encoding(self, arg):
    self.write("DAT:ENC %s" % arg)
  
  #1, 2
  def data_width(self, arg):
    self.write("DAT:WID %s" % arg)

  #number of first sample, starting at 1
  def data_start(self, arg):
    self.write("DAT:STAR %s" % arg)

  #last sample to transmit, max 10000
  def data_stop(self, arg):
    self.write("DAT:STOP %s" %arg)

  def waveform(self):
    return self.ask_raw(b"WAVF?")

