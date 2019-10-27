# DIY Wilma Robot

### Background

After building some construction on the garden my 4 year old daughter and I built a small robot of some spare wood planks :hammer: 
I've tried to explain to her that daddy builds robots at his work ... perhaps not entirely accurate though :grin:
So quite naturally thinking we'll need to give this robot a brain :bulb: .. this might be a fun [DIY](https://en.wikipedia.org/wiki/Do_it_yourself) (Do It Yourself) project
that might be fun and share for inspiration :smirk:

While my daughter have her boxes with toys so did luckily her dad .. so was just a matter start using the soldering iron ..
I'll explain below what items were needed and how to glue these together, 
if you feel uncomfortable soldering you may instead purchase a [breadboard](https://www.aliexpress.com/item/1893684840.html) instead.
The cost for such project shouldn't have to cost more than a tiny 10 euros.

And finally I'll have written some MicroPython :snake: for those who doesn't know is a [Python](https://en.wikipedia.org/wiki/Python_(programming_language)
implementation optimized to run on microcontrollers. 

### Material list

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
| spare woods and nails   	| for free?        	|                                                    	|
|                         	|                  	|                                                    	|
| Total cost              	| 9                	|                                                    	|

### How to wire the components


### How to configure and upload the software

- Follow [these](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) instructions to upload MicroPython to your ESP32

- Update the following lines in main.py
```python
# Configure your wifi

WIFI_SSID = 'xxxx'
WIFI_PASS = 'xxxx'
```

- Upload the following files to the ESP32 flash using e.g. ampy described better [here](https://boneskull.com/micropython-on-esp32-part-1/).
    - jq6500.py
    - main.py


### Upload voice prompts

Connect the jq6500 module to available USB and it will open a "downloader" (on Windows) and you can then
upload all prompts found in the **voice_prompts** folder. More details and hints could be found [here](https://sparks.gogo.co.nz/jq6500/index.html).

### The final result
