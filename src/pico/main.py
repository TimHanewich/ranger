import machine
import time

uart = machine.UART(0, baudrate=9600, tx=machine.Pin(16))
adc = machine.ADC(26)

while True:

    # read
    print("Reading...")
    input = adc.read_u16()
    print("Read value '" + str(input) + "'")

    # transmit
    ToTransmit:str = str(input) + "\r\n"
    print("Transmitting via UART... ")
    uart.send(ToTransmit.encode())
    print("Transmitted!")

    # wait
    time.sleep(1.0)