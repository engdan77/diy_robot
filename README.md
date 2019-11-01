# DIY Robot

<img src="https://vignette.wikia.nocookie.net/kalleankasverige/images/7/73/Oppfinnar-Jocke.gif/revision/latest?cb=20130720090538&path-prefix=sv" width="80">

### Background
After building some construction on the garden my 4 year old daughter and I built a small robot of some spare wood planks :hammer: 
I've tried to explain to her that daddy builds robots at his work ... perhaps not entirely accurate though :grin:
So quite naturally thinking we'll need to give this robot a brain :bulb: .. this might be a fun [DIY](https://en.wikipedia.org/wiki/Do_it_yourself) (Do It Yourself) project
that might be fun and share for inspiration :smirk:

While my daughter have her boxes with toys so did luckily her dad .. so was just a matter start using the soldering iron ..
I'll explain below what items were needed and how to glue these together, 
if you feel uncomfortable soldering you may instead purchase a [breadboard](https://www.aliexpress.com/item/1893684840.html) instead.
The cost for such project shouldn't have to cost more than a 10 euros which I personally is not too shabby for a talking/seeing wifi-connected robot :money_with_wings: :yum:

And finally I'll have written some MicroPython :snake: for those who doesn't know is a [Python](https://en.wikipedia.org/wiki/Python_(programming_language)
implementation optimized to run on microcontrollers. 

### How does the robot work?
Thanks to ESP32 capacitive touch GPIOs we can pull a wire to e.g. a screw/coin that is able to sense touches instead of using mechanical buttons.
We have the following buttons that tells the robot the following

- **Button 1 - play hide'n seek**
    - The robot will ask you to stand in the middle of the room and will challenge you to be as still as you can for 30 seconds.
    If the robot find your movement it wins otherwise you will..
- **Button 2 - tell time and day**
    - The robot establishes connection to Wifi and connects to WorldClock API cycling between saying what day it is or what hour of the day it is (CET)... I thought of introducing "it is bedtime for you now".
- **Button 3 - tell what weather it is outside**
    - The robots use Wifi and connects to api.met.no to determine the weather based on the WEATHERLOCATION defined and reads wether is sun, rain, cloud, thunder and so on.
- **Button 4 - reads out the magic word**
    - "poop"
- **Button 3 + 4 simultaneous - wifi and webrepl**
    - If you like to have the robot connect to your wifi and enable [webrepl](https://docs.micropython.org/en/latest/esp8266/tutorial/repl.html) that allows you to e.g. interactively control the robot and upload/download files.
      

### The final result
You can check out this video to see what the result might look like..
<a href="https://www.youtube.com/watch?v=Bjfdz-HMM34&cc_lang_pref=en"><img src="https://github.com/engdan77/diy_robot/raw/master/docs/play.png" width="300"></a>


### Make your own robot


#### Material list

| ﻿Item                    	| appr. Cost (EUR) 	| URL to item                                        	|
|-------------------------	|------------------	|----------------------------------------------------	|
| mini-slide-switch       	| 0,05             	| https://www.aliexpress.com/item/32807751467.html   	|
| 0,5 ohm speaker         	| 0,5              	| https://www.aliexpress.com/item/32814341548.html   	|
| jq6500                  	| 1,5              	| https://www.aliexpress.com/item/32718352583.html   	|
| PIR (SR501)             	| 0,8              	| https://www.aliexpress.com/item/32243592989.html   	|
| ESP32                   	| 3,5              	| https://www.aliexpress.com/item/32928267626.html   	|
| 10u capacitor           	| 0,5              	| https://www.aliexpress.com/item/4000096483128.html 	|
| wires                   	| 0,5              	| https://www.aliexpress.com/item/32969382424.html   	|
| 9v battery holder       	| 0,2              	| https://www.aliexpress.com/item/32837950993.html   	|
| 2 pcs green leds        	| 0,2              	| https://www.aliexpress.com/item/32999447594.html   	|
| 2 pcs 200 ohm resistors 	| 0,2              	| https://www.aliexpress.com/item/32868810758.html   	|
| PCB board               	| 0,2              	| https://www.aliexpress.com/item/32961983574.html   	|
| spare wood, nails/screws  | for free(?)       |                                                    	|
|                         	|                  	|                                                    	|
| Total cost              	| 9                	|                                                    	|

#### How to wire the components
You have the sketch and wiring found under the docs directory..
<a href="https://github.com/engdan77/diy_robot/raw/master/docs/robot_sketch.png">"<img src="https://github.com/engdan77/diy_robot/raw/master/docs/robot_sketch.png" width="600"></a>

#### How to configure and upload the software

- Follow [these](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) instructions to upload MicroPython to your ESP32

- Update the following lines in main.py

```python
# Configure your wifi

WIFI_SSID = 'xxxx'
WIFI_PASS = 'xxxx'

# Used to tell what the weather it is
WEATHERLOCATION = 'lat=57.8813&lon=13.784'
```

- Upload the following files to the ESP32 flash using e.g. ampy described better [here](https://boneskull.com/micropython-on-esp32-part-1/).
    - jq6500.py
    - main.py


#### Upload voice prompts

Connect the jq6500 module to available USB and it will open a "downloader" (on Windows) and you can then
upload all prompts found in the "voice_prompts" folder, I'd suggest you come up with your own voice prompts unless you'd like to keep these swedish ones and you'd pretty much find what being said in the code

```python
# Slot in JQ6500 vs voice prompt mapping
MyVoices = namedtuple('MyVoices', 'welcome '
                                  'i_see_you '
                                  'now_we_play '
                                  'instruct_hide '
                                  'now_stand_still .....')
# and so on
```
More details and hints could be found [here](https://sparks.gogo.co.nz/jq6500/index.html).


