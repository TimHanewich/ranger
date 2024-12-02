import machine
import time

# set up
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(16))
adc = machine.ADC(26)

# turn on LED while working properly
led = machine.Pin("LED", machine.Pin.OUT)
led.on()

try:
    while True:
        
        # read
        print("Reading...")
        input = adc.read_u16()
        print("Read value '" + str(input) + "'")

        # transmit
        ToTransmit:str = str(input) + "\r\n"
        print("Transmitting via UART... ")
        uart.write(ToTransmit.encode())
        print("Transmitted!")

        # wait
        time.sleep(1.0)
except Exception as ex:
    print("Fatal error! Msg: " + str(ex))
    print("Now playing error LED pattern.")
    while True:
        led.on()
        time.sleep(1.0)
        led.off()
        time.sleep(1.0)