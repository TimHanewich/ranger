import psutil
import settings
import json
from azure.storage.queue import QueueClient

def prepare() -> dict:
    """Prepares a return packet with the standard inclusions"""

    ToReturn:dict = {}

    # get memory info
    meminfo = psutil.virtual_memory()
    ToReturn["memp"] = round(meminfo.percent / 100, 3) # memory used, as a percent of total memory
    ToReturn["memu"] = meminfo.used # memory used, in bytes
    ToReturn["mema"] = meminfo.available # memory available, in bytes

    # get disk info
    du = psutil.disk_usage("/")
    ToReturn["diska"] = du.free

    # get network io information
    netio = psutil.net_io_counters()
    ToReturn["bsent"] = netio.bytes_sent
    ToReturn["brecv"] = netio.bytes_recv

    # return it
    return ToReturn


def send(msg:dict) -> None:
    """Sends a message via queue storage"""
    qc = QueueClient.from_connection_string(_getazconstr(), "r2c")
    try: # try to create. If it fails, it must already exist
        qc.create_queue()
    except:
        pass
    qc.send_message(json.dumps(msg))

def _getazconstr() -> str:
    f = open("../azure_connection_string.txt", "rt")
    ToReturn:str = f.read()
    f.close()
    return ToReturn
    