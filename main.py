import machine
from machine import Pin, TouchPad
import utime
from jq6500 import Player
import webrepl
import network
from ucollections import namedtuple
import esp32
import urequests

MyPins = namedtuple('MyPins', 'left_eye right_eye pir b1 b2 b3 b4')
o = MyPins(left_eye=22,
           right_eye=23,
           pir=21,
           b1=33,
           b2=12,
           b3=13,
           b4=15)

MyVoices = namedtuple('MyVoices', 'welcome '
                                  'i_see_you '
                                  'now_we_play '
                                  'instruct_hide '
                                  'now_stand_still '
                                  'bajsoppa '
                                  'today_it_is '
                                  'sunny '
                                  'cloudy '
                                  'sleet'
                                  'fog'
                                  'thunder'
                                  'monday'
                                  'tuesday'
                                  'wednesday'
                                  'thursday'
                                  'friday'
                                  'saturday'
                                  'sunday'
                                  '1'
                                  '2'
                                  '3'
                                  '4'
                                  '5'
                                  '6'
                                  '7'
                                  '8'
                                  '9'
                                  '10'
                                  '11'
                                  '12'
                                  'i_won'
                                  'you_won'
                                  'i_am_hot'
                                  'music')
v = MyVoices(*list(range(1, 34)))


class MyTouchButtons:
    def __init__(self, pins, sensitivity=600, threshold=0.2):
        self.pins = pins
        self.sensitivity = sensitivity
        self.threshold = threshold
        self.default = []
        self.default = self.read()

    def read(self):
        r = {}
        for p in self.pins:
            t = TouchPad(Pin(p))
            t.config(self.sensitivity)
            v = t.read()
            r[p] = v
        return r

    def get_score(self, reading, default):
        return abs(1 - reading / default)

    def pressed(self, verbose_output=False):
        pins = []
        verbose = ''
        for pin, reading, default in zip(self.pins, self.read().values(), self.default.values()):
            score = self.get_score(reading, default)
            verbose += 'pin:{} read:{} def:{}, score: {}    '.format(pin, reading, default, score)
            if score > self.threshold:
                pins.append(pin)
        if verbose_output:
            print(verbose)
        return pins


class MyTempSensor:
    def __init__(self, temp_diff=5):
        self.initial = self.read()
        self.triggered = False
        self.temp_diff = temp_diff

    def read(self):
        f = esp32.raw_temperature()
        c = (f - 32) / 1.8
        return c

    def warm(self):
        if self.triggered:
            return False
        current = self.read()
        diff = abs(current / self.initial)
        if diff >= self.temp_diff:
            return True
        return False


class MyVoice:
    def __init__(self, cycle_functions=[]):
        self.current = 0
        self.cycle_functions = cycle_functions

    def talk(self):
        self.cycle_functions[self.current]()
        if self.current >= len(self.cycle_functions):
            self.current = 0
        else:
            self.current += 1


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


def get_weather():
    url = 'https://api.met.no/weatherapi/locationforecast/1.9/?lat=57.8813&lon=13.784'
    filename = 'weather.xml'
    with open(filename, 'w') as f:
        f.write(urequests.get(url).text)
    x = xmltok.tokenize(open(filename))
    found = None
    try:
        while True:
            n = next(x)
            if 'START_TAG' in n and 'symbol' in n[1]:
                found = next(x)[-1]
                break
    except StopIteration:
        pass
    return found.lower()


def say_hour():
    print('current hour is ...')
    print(get_hour())


def get_weekday():
    url = 'http://worldclockapi.com/api/json/cet/now'
    a = urequests.get(url).json()
    return a['dayOfTheWeek'].lower()


def get_hour():
    url = 'http://worldclockapi.com/api/json/cet/now'
    h = urequests.get(url).json()['currentDateTime'][11:13]
    h = int(h) if int(h) <= 12 else int(h) - 12
    return str(h)


def say_weekday():
    print('Current day is...')
    audio_map = {'monday': 1,
                 'tuesday': 2,
                 'wednesday': 3,
                 'thursday': 4,
                 'friday': 5,
                 'saturday': 6,
                 'sunday': 7}
    w = get_weekday()
    print('weekday: {}'.format(audio_map[w]))


def say_weather():
    print('The time is ...')
    audio_map = {'sun': 1,
                 'rain': 2,
                 'snow': 3,
                 'sleet': 4,
                 'fog': 5,
                 'thunder': 6}
    current_weather = get_weather()
    for k, v in audio_map.items():
        if current_weather in k:
            print('weather: {}'.format(v))


def motion_detected(pir_pin):
    p = Pin(pir_pin, Pin.IN).value()
    # import random
    # p = not bool(random.randrange(0, 100))
    return p


def play_hide(pir_pin, max_secs=30, interval_ms=20):
    play_audio(v.now_we_play)
    play_audio(v.instruct_hide)
    max_times = (max_secs * 1000) / interval_ms
    current_time = 0
    see_you = False

    utime.sleep(3)
    play_audio(v.now_stand_still)
    while current_time <= max_times and not see_you:
        if see_you:
            print('I see you !!')
            play_audio(v.i_see_you)
            break
        utime.sleep_ms(interval_ms)
        see_you = motion_detected(pir_pin)
        current_time += 1
    print(current_time)
    if not see_you:
        for _ in range(10):
            light_on(True, pin=o.left_eye)
            light_on(False, pin=o.right_eye)
            utime.sleep(0.1)
            light_on(False, pin=o.left_eye)
            light_on(True, pin=o.right_eye)
        light_on(False, pin=[o.left_eye, o.right_eye])
        print('I give up! You win..')
    else:
        blink([o.left_eye, o.right_eye], times=10, sleep=0.01)
        play_audio(v.i_see_you)
        print('I see you, I win')


def loop_input():
    temp = MyTempSensor(5)
    voice = MyVoice([say_weekday, say_weather, say_hour])
    touch = MyTouchButtons([o.b1, o.b2, o.b3, o.b4])
    while True:
        utime.sleep_ms(20)
        if o.b1 in touch.pressed():
            print('button 1')
            blink([o.left_eye, o.right_eye])
            print('let us play')
            blink(times=20, sleep=0.01)
            play_hide(o.pir)
        if o.b3 in touch.pressed():
            print('button 3')
            blink([o.left_eye, o.right_eye])
            play_audio(v.bajsoppa)
            wifi_connect()
            voice.talk()
        if o.b4 in touch.pressed():
            print('button 4')
            blink()
            light_on(False, pin=[o.left_eye, o.right_eye])
            utime.sleep(5)
            wifi_connect()
            webrepl.start(8266, password='secret')
        if temp.warm():
            blink([o.left_eye, o.right_eye], times=20, sleep=0.01)
            print('I am warm')

def main():
    play_audio(1)
    loop_input()

main()
