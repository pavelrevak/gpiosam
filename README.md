# gpio_sam
Python fast GPIO driver for Atmel AT91SAM MCUs

This class need root privileges, because it use direct memory access.

Examples:
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
