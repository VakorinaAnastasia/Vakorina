import RPi.GPIO as GPIO

dac = [8, 11, 7, 1, 0, 5, 12, 6]
bits = len(dac)
maxVolt = 3.3
levels = 2**bits
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.output(dac, GPIO.LOW)

def decimal_to_bin(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

try:
    while True:
        user_input = input('Введите целое число от 0 до 225:')

        if user_input.lower() == 'q':
            break
        
        try:
            decimal_val = int(user_input)

        except ValueError:
            print('Ошибка: введите целое число или q')
            continue

        if decimal_val < 0:
            print('Ошибка: введите положительное число')
            continue

        if decimal_val > 255:
            print('Ошибка: введите число, не превышающее 255')
            continue

        binary_val = decimal_to_bin(decimal_val)
        GPIO.output(dac, binary_val)

        voltage = maxVolt * decimal_val / (levels - 1)
        print(voltage)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()





