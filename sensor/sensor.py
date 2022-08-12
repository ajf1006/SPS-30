#!/usr/bin/env python
# coding: utf-8


import serial.tools.list_ports as list_ports
import serial
from time import sleep
import struct
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()

start_meas = bytearray([0x7E,0x00,0x00,0x02,0x01,0x03,0xF9,0x7E])
read_meas = bytearray([0x7E,0x00,0x03,0x00,0xFC,0x7E])
stop_meas = bytearray([0x7E,0x00,0x01,0x00,0xFE,0x7E])
fan_clean = bytearray([0x7E,0x00,0x56,0x00,0xA9,0x7E])

def unstuff(raw):
    if b'\x7D\x5E' in raw:
        raw = raw.replace(b'\x7D\x5E', b'\x7E')
    if b'\x7D\x5D' in raw:
        raw = raw.replace(b'\x7D\x5D', b'\x7D')
    if b'\x7D\x31' in raw:
        raw = raw.replace(b'\x7D\x31', b'\x11')
    if b'\x7D\x33' in raw:
        raw = raw.replace(b'\x7D\x33', b'\x13')
    return raw

def start_SPS30(wait_time):
    ports = list_ports.comports()
    print(ports)
    for port in ports:
        if 'UART' in str(port):
            port_name = str(port).split(' ')[0]
    ser = serial.Serial(port_name,baudrate=115200,bytesize=8,parity='N',stopbits=1)
    ser.flushInput()
    ser.write(start_meas)
    sleep(wait_time)
    in_waiting = ser.in_waiting
    in_data = ser.read(in_waiting)
    error = in_data[3]
    return ser,error

def meas_SPS30(ser):
    ser.write(read_meas)
    sleep(0.1)
    in_waiting = ser.in_waiting
    raw = ser.read(in_waiting)
    sleep(0.1)
    error = raw[3]
    raw = unstuff(raw)
    raw = raw[5:-2]
    try:
        in_data = struct.unpack(">ffffffffff",raw)
    except:
        in_data = [0,0,0,0]
    return in_data[0],in_data[3],error

def stop_SPS30(ser):
    ser.write(stop_meas)
    sleep(1)
    in_waiting = ser.in_waiting
    in_data = ser.read(in_waiting)
    error = in_data[3]
    return error

def clean_SPS30(ser):
    ser.write(fan_clean)
    sleep(1)
    in_waiting = ser.in_waiting
    in_data = ser.read(in_waiting)
    error = in_data[3]
    return errror

def send_data(pm2pt5,pm10,address):
    t = time.time()
    date_now = time.strftime('%Y-%m-%d',time.localtime(t))
    time_now = time.strftime('%H-%M',time.localtime(t))
    
    payload = {'date':date_now,'time':time_now,'pm2pt5':pm2pt5,'pm10':pm10}
    r = requests.get(address,payload)
    print(r.url)
    print(r.status_code)
    with open('test.txt','a') as f:
        f.write(r.url)
        f.write('\n')
    
def meas_av(ser,samples):
    pm2pt5 = []
    pm10 = []
    for i in range(samples):
        out2pt5=0
        while out2pt5<0.01:
            sleep(0.1)
            out2pt5,out10,error = meas_SPS30(ser)
        pm2pt5.append(out2pt5)
        pm10.append(out10)
    '''print('pm2pt5 {:.1f} ug/m3'.format(out2pt5))
    print('pm10 {:.1f} ug/m3'.format(out10))'''

    pm2pt5_av = round(sum(pm2pt5)/samples,2)
    pm10_av = round(sum(pm10)/samples,2)
    return pm2pt5_av,pm10_av

def main():
    ser,error = start_SPS30(5)
    samples = 2
    pm2pt5_av,pm10_av = meas_av(ser,samples)
    address = 'http://ajf1006@pythonanywhere.com/receive-data'
    send_data(pm2pt5_av,pm10_av,address)
    stop_SPS30(ser)

job = scheduler.add_job(main,'cron',minute=10)
scheduler.start()
while True:
    sleep(1)
