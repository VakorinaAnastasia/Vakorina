import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

dac = [8, 11, 7, 1, 0, 5, 12, 6] 
leds = [2, 3, 4, 17, 27, 22, 10, 9] 
comp = 14
troyka = 13

uref = 3.3 
max_val = 255  
target_charge = 0.97
target_discharge = 0.02
high = 2.67
low = uref * target_discharge


GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT)


def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def light_up(value):
    led_output = decimal2binary(value)
    GPIO.output(leds, led_output)

def adc():
    value = 0
    for i in range(7, -1, -1):
        value += 2**i
        signal = decimal2binary(value)
        GPIO.output(dac, signal)
        time.sleep(0.01)
        if GPIO.input(comp) == 1:
            value -= 2**i
    return value

def measure_voltage(digital_value):
    return uref * digital_value / max_val

def light_up_binary(value):
    binary_representation = decimal2binary(value)
    GPIO.output(leds, binary_representation)

measurements = []

try:
    start_time = time.time()

    print("Зарядка конденсатора")
    GPIO.output(troyka, GPIO.HIGH)  
    voltage = 0
    while voltage < high:
        digital_value = adc()  
        voltage = measure_voltage(digital_value)
        measurements.append(digital_value)
        light_up_binary(digital_value)  
        print(f"Напряжение: {voltage:.2f} В")

    print("Разрядка конденсатора")
    GPIO.output(troyka, GPIO.LOW) 
    voltage = uref 
    while voltage > low:
        digital_value = adc() 
        voltage = measure_voltage(digital_value)
        measurements.append(digital_value)
        light_up_binary(digital_value) 
        print(f"Напряжение: {voltage:.2f} В")

    end_time = time.time()
    duration = end_time - start_time

    num_measurements = len(measurements)
    sampling_rate = num_measurements / duration if duration > 0 else 0
    quantization_step = uref / max_val

    plt.plot(measurements)
    plt.xlabel("Номер измерения")
    plt.ylabel("Значение АЦП")
    plt.title("Значения АЦП во время зарядки и разрядки")
    plt.grid(True)
    plt.savefig("adc_plot.png") 
    plt.show()

    with open("new_data.txt", "w") as f:
        for value in measurements:
            f.write(str(value) + "\n")

    with open("settings.txt", "w") as f:
        f.write(f"Частота дискретизации: {sampling_rate:.2f} Гц\n")
        f.write(f"Шаг квантования: {quantization_step:.4f} В")

    print(f"Общая продолжительность: {duration:.2f} секунд")
    print(f"Количество измерений: {num_measurements}")
    print(f"Период измерения: {1/sampling_rate:.4f} секунд")
    print(f"Частота дискретизации: {sampling_rate:.2f} Гц")
    print(f"Шаг квантования: {quantization_step:.4f} В")

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(leds, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)  
    GPIO.cleanup()
