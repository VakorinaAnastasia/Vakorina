import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT) 
GPIO.setup(troyka, GPIO.OUT, initial=0)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def light_up(value):
    led_output = decimal2binary(value)
    GPIO.output(leds, led_output)

# def adc_1():
#     for value in range(256):
#         signal = decimal2binary(value)
#         GPIO.output(dac, signal)
#         time.sleep(0.001)
#         if GPIO.input(comp) == 1:
#             return value
#     return 255

def adc_2():
    value = 0
    for i in range(7, -1, -1):
        value += 2**i
        signal = decimal2binary(value)
        GPIO.output(dac, signal)
        time.sleep(0.001)
        if GPIO.input(comp) == 0:
            value -= 2**i
    return value 

try:
    while True:
        digital_value = adc_2()
        led_value = digital_value // 32 
        led_value = min(max(round(led_value),0),7)
        to_light = [1 if i < led_value else 0 for i in range(8)]
        GPIO.output(leds, to_light) 
        print(f"Digital Value (цифровое значение): {digital_value}")
        time.sleep(0.1) 
finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()