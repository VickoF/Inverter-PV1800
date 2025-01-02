import minimalmodbus

# Настроим клиент Modbus
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # адрес устройства 1
instrument.serial.baudrate = 115200  # скорость
instrument.serial.bytesize = 8    # размер байта
instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.timeout = 0.5  # Тайм-аут в секундах

# Чтение 75 регистров начиная с 25200
try:
    registers = instrument.read_registers(25200, 75, 3)
    print(registers)
except minimalmodbus.NoResponseError:
    print("No response from device")
