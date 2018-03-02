#!/usr/bin/python
import can
import time
import RPi.GPIO as GPIO
import threading
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_UP)
can.rc['interface'] = 'socketcan_ctypes'
can.rc['channel'] = 'can0'
from can.interfaces.interface import *
bus = can.interface.Bus(channel='can0' , bustype='socketcan_ctypes')
can_send_lock = threading.Lock() #Needed to synchronize CAN-Transceiver requests

class CAN (threading.Thread):
    def __init__(self, message, period):
        threading.Thread.__init__(self)
        self.message = message
        self.period = period
        self.active = 1
    def run(self):
       TIMER = 0
       while self.active==1:
          if TIMER%self.period==0 and TIMER>0:
             can_send(self.message)
          time.sleep(0.001)
          TIMER=TIMER+1
    def stop(self):
       self.active=0
          
def can_send(message):
   with can_send_lock:
      bus.send(message)

#-----------------------------WRITE YOUR CAN SIMULATION BELOW HERE (Dont change code above this line)!-----------------------------------------------------------------------

# DEFINE ALL INITIAL CAN MESSAGES: "CAN(can.Message(arbitration_id=ID, dlc=data lenght code, data=[0,0,0,...], extended_id=false or true, period in ms) 
MSG_1 =        CAN(can.Message(arbitration_id=0x12, dlc=8, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False), 10)
MSG_2 = CAN(can.Message(arbitration_id=0x30, dlc=8, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False),15)
MSG_3 =    CAN(can.Message(arbitration_id=0x38, dlc=8, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False),15)

# Start periodic Msg sending
MSG_1.start()
MSG_2.start()
MSG_3.start()

# Change Message Data if Button 23 is pressed / Stop simulation if Button 24 is pressed
while 1:
    if (GPIO.input(23)==0):
	print "Messages contain data"
        MSG_1.message = can.Message(arbitration_id=0x12, dlc=8, data=[0, 0, 0, 0, 0, 7, 0, 0], extended_id=False)
        MSG_2.message = can.Message(arbitration_id=0x30, dlc=8, data=[128, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
        MSG_3.message = can.Message(arbitration_id=0x38, dlc=8, data=[0, 0, 0, 0, 0, 32, 0, 0], extended_id=False)
    else:
	print "Messages contain zeros"
        MSG_1.message = can.Message(arbitration_id=0x12, dlc=8, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
        MSG_2.message = can.Message(arbitration_id=0x30, dlc=8, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
        MSG_3.message = can.Message(arbitration_id=0x38, dlc=8, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)

    if (GPIO.input(24)==0):
        MSG_1.stop()
        MSG_2.stop()
        MSG_3.stop()
        break
