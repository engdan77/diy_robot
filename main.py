import machine
from machine import Pin, TouchPad
import utime
from jq6500 import Player
import webrepl
import network
from ucollections import namedtuple

MyPins = namedtuple('MyPins', 'left_eye right_eye pir b1 b2 b3 b4 b5')
o = MyPins(left_eye=22,
           right_eye=23,
           pir=24,
           b1=2,
           b2=25,
           b3=12,
           b4=13,
           b5=15)

WIFI_SSID = '***REMOVED***'
WIFI_PASS = '***REMOVED***'


def read_touch(pins=(13, 12, 14, 27, 33, 32, 15, 4), sensitivity=600):
    r = {}
    for p in pins:
        t = TouchPad(Pin(p))
        t.config(sensitivity)
        v = t.read()
        r[p] = v
    return r


def play_audio(index=1, blocking=True, max_length=20):
    p = Player(port=2)
    utime.sleep(0.5)
    p.set_volume(30)
    utime.sleep(0.5)
    p.play_by_index(index)
    if blocking:
        for _ in range(max_length):
            utime.sleep(1)
            if not p.get_status() == p.STATUS_PLAYING:
                break
    p.clean_up()


def blink(pin=2, times=6, sleep=0.2):
    pin = [pin] if type(pin) is int else pin
    for q in pin:
        p = machine.Pin(q, machine.Pin.OUT)
        for _ in range(times):
            p.value(not p.value())
            utime.sleep(sleep)


def light_on(on=True, period=None, pin=2):
    pin = [pin] if type(pin) is int else pin
    for q in pin:
        machine.Pin(q, machine.Pin.OUT).value(bool(on))
    if period:
        utime.sleep(period)
        for q in pin:
            machine.Pin(q, machine.Pin.OUT).value(False)


def restart_wifi(sta_if):
    sta_if.disconnect()
    sta_if.active(False)
    utime.sleep(1)
    sta_if.active(True)
    utime.sleep(1)
    sta_if.connect(WIFI_SSID, WIFI_PASS)


def wifi_connect(pin_working=22, pin_connected=23):
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        print("Already connected")
        return
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASS)
    repeats = 0
    while not sta_if.isconnected():
        repeats += 1
        utime.sleep(0.3)
        light_on(True, 0.2, pin_working)
        if repeats >= 8:
            repeats = 0
            restart_wifi(sta_if)
    light_on(True, None, pin_connected)


def loop_input():
    blink([o.left_eye, o.right_eye])
    while True:
        utime.sleep_ms(50)
        b = read_touch()
        if b[o.b5] < 400:
            blink(times=20, sleep=0.05)
            play_audio(2)


def main():
    light_on(True, pin=[o.left_eye, o.right_eye])
    play_audio(1)
    utime.sleep(5)
    wifi_connect()
    webrepl.start(8266, password='secret')
    loop_input()


main()
