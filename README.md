# gpio_sam
Python fast GPIO driver for Atmel AT91SAM MCUs

This class need root privileges, because it use direct memory access.

request python v2.7 or v3.x

##Examples:
```python
import gpio_sam
btn = gpio_sam.Gpio('A', 27)
btn.enable = True
btn.output_mode = False
btn.pull_up = False
btn.pull_down = True
btn.input
  False
btn.input
  True
led = gpio_sam.Gpio('A', 26)
led.enable = True
led.output_mode = True
led.output = True
led.output
  True
led.output = False
led.output
  False
led.output = not led.output
led.output
  True
```
##API:
###Gpio(port, pin)
initialize GPIO on *port* and *pin*

###Gpio.enable
property (rw) to enable or disable gpio

###Gpio.output_mode
property (rw) *true* to configure GPIO as output or *false* as input

###Gpio.open_drain
property (rw) to configure GPIO as open drain if is as outpu

###Gpio.pull_up
property (rw) control pull up resistors

###Gpio.pull_down
property (rw) control pull down resistors

###Gpio.output
property (rw) to control output on GPIO

###Gpio.input
property (r) to read GPIO value
