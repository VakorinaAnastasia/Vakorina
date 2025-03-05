import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]  
comp = 4  
troyka = 17  

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=0)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
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
       digital_value = adc()
       voltage = 3.3 * digital_value / 256
       print(f"Digital Value (цифровое значение): {digital_value}, Напряжение: {voltage} В")
       time.sleep(0.1)


finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
