import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
bits = len(dac)
maxVolt = 3.3
levels = 2**bits
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.output(dac, GPIO.LOW)

def dec2bin(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

try:
    period = float(input('Задайте период треугольного сигнала:'))
    step_delay = period / (2 * levels)

    while True:
        for value in range(levels):
            signal = dec2bin(value)
            GPIO.output(dac, signal)
            time.sleep(step_delay)

        for value in range (levels - 1, -1, -1):
            signal = dec2bin(value)
            GPIO.output(dac, signal)
            time.sleep(step_delay)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()