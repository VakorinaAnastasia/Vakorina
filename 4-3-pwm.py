import RPi.GPIO as GPIO
import time

pwm_pin = 18 

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.OUT)

pwm_frequency = 1000
pwm = GPIO.PWM(pwm_pin, pwm_frequency)

try:
    pwm.start(0)

    while True:
        duty_cycle = float(input('Введите коэффициент заполнения 0-100:'))

        if 0 <= duty_cycle <= 100:
            pwm.ChangeDutyCycle(duty_cycle) 
            maxVolt = 3.3
            volt = (duty_cycle / 100) * maxVolt
            print(f"Напряжение: {volt}В")

finally:
    pwm.stop()
    GPIO.cleanup()
