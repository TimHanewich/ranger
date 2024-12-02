import serial
import BatteryMonitor

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
        
    def voltage(self) -> float:
        """Interprets the voltage of the battery and returns it as a floating point number"""

        # RESEARCH
        # The voltage of the battery is passed through a voltage divider, read by a Raspberry Pi Pico (on an ADC pin), and then transmitted to the Raspberry Pi Zero via UART.
        # Thus, we have to interpret the raw ADC reading passed from the pico and turn this into a voltage reading
        # screenshot of basic code test I set up, supplying power through an adjustable DC power supply: https://i.imgur.com/U85zUfs.png
        # 
        # Raw integer (ADC) reading, passed from Pico, for various supply voltages (emulating a 4S LiPo):
        # @ 16.8V supply (100% charged 4S LiPo) = 57,093
        # @ 15.8V supply (75% charged 4S LiPo) = 54,053
        # @ 15.4V supply (50% charged 4S LiPo) = 52,498
        # @ 14.6V supply (25% charged 4S LiPo) = 49,679
        # @ 12.0V supply (0% charged 4S LiPo) = 40,994

        # read raw
        raw:int = self._read_raw()

        # convert to voltage estimate
        PercentOfRange:float = (raw - 40994) / (57093 - 40094)
        volts:float = 12.0 + ((16.8 - 12.0) * PercentOfRange)
        return volts
        
    
    def close(self) -> None:
        """Closes the serial connection."""
        self.ser.close()