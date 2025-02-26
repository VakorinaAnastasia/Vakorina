import RPi.GPIO as GPIO
import time

pwm_pin = 20
#led_pin = 9
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.OUT)
#GPIO.setup(led_pin, GPIO.OUT)

pwm_frequency = 1000
pwm = GPIO.PWM(pwm_pin, pwm_frequency)

try:
    while True:
        duty_cycle = float(input('Введите коэффициент заполнения 0-100:'))

        if 0 <= duty_cycle <= 100:
#            period = 0.001
#            on_time = period * (duty_cycle / 100)
#            off_time = period - on_time


            GPIO.output(pwm_pin, GPIO.HIGH)
#            GPIO.output(led_pin, GPIO.HIGH)
#            time.sleep(on_time)

            GPIO.output(pwm_pin, GPIO.LOW)
#            GPIO.output(led_pin, GPIO.LOW)
#            time.sleep(off_time)

            maxVolt = 3.3
            volt = (duty_cycle / 100) * maxVolt
            print(volt) 

        else:
            print('Коэффициент заполнения должен быть от 0 до 100')


finally:
    GPIO.cleanup()