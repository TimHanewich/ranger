import serial

class VoltageSensor:

    def __init__(self, bus:str = "/dev/serial0", baudrate:int = 9600):
        self.ser:serial.Serial = serial.Serial(bus, baudrate)

    def _read_raw(self) -> int:
        """Reads the raw integer value coming through on the UART"""
        next:bytes = self.ser.readline()
        nexts:str = next.decode()
        nexts = nexts.replace("\r\n", "")
        nexti:int = int(nexts) # convert
        return nexti    
    
    def close(self) -> None:
        """Closes the serial connection."""