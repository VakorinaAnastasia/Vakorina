import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]  
comp = 14  
troyka = 13  

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=0)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    for value in range(256):
        signal = decimal2binary(value)
        GPIO.output(dac, signal)
        time.sleep(0.01)
        if GPIO.input(comp) == 1:
            return value
    return 255 

#try:
#    while True:
#        digital_value = adc()
#        voltage = 3.3 * digital_value / 256
#        print(f"Digital Value (цифровое значение): {digital_value}, Напряжение: {voltage} В")
#        time.sleep(0.1)

try:
    start_time = time.time()
    num_iterations = 100 
    sum_of_voltages = 0
    for _ in range(num_iterations):
        digital_value = adc()
        voltage = 3.3 * digital_value / 256
    end_time = time.time()
    avg_time = (end_time - start_time) / num_iterations
    print(f"Среднее время работы алгоритма: {avg_time} секунд")

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()

