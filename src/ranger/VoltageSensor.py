import serial

class VoltageSensor:

    def __init__(self, bus:str = "/dev/serial0", baudrate:int = 9600):
        self.ser:serial.Serial = serial.Serial(bus, baudrate)

    def _read_raw(self) -> int:
        """Reads the raw integer value coming through on the UART"""
        if self.ser.is_open:
            self.ser.reset_input_buffer() # clear the RX buffer so that way we know what we are about to read is brand new data
            next:bytes = self.ser.readline()
            nexts:str = next.decode()
            nexts = nexts.replace("\r\n", "")
            nexti:int = int(nexts) # convert
            return nexti    
        else:
            raise Exception("Cannot read voltage because the serial connection was closed!")
    
    def close(self) -> None:
        """Closes the serial connection."""
        self.ser.close()