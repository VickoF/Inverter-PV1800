import minimalmodbus
import sys

# Параметры командной строки
device_id = int(sys.argv[1])  # Идентификатор устройства (из параметра командной строки)
baud_rate = int(sys.argv[2])  # Скорость передачи данных (из параметра командной строки)

# Константы
SERPORT = '/dev/ttyUSB0'  # Путь к последовательному порту
SERTIMEOUT = 0.5          # Таймаут в секундах
SERBAUD = baud_rate       # Устанавливаем скорость порта

# Создание объекта для Modbus
i = minimalmodbus.Instrument(SERPORT, device_id)
i.serial.timeout = SERTIMEOUT
i.serial.baudrate = SERBAUD

# Чтение регистров
registers_from = 15200
registers_count = 10

try:
    # Чтение регистров с устройства
    results = i.read_registers(registers_from, registers_count)
    
    # Вывод результатов
    for i, v in enumerate(results):
        print(f"Register {i + registers_from} = {v}     ->     index  [ {i+1} ]")

except Exception as e:
    print(f"Ошибка при чтении данных: {e}")

