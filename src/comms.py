import psutil
import settings
import json
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage, BinaryBase64DecodePolicy, BinaryBase64EncodePolicy

def prepare() -> dict:
    """Prepares a return packet"""

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
    qc = QueueClient.from_connection_string(settings.azure_storage_constr, "r2c")
    try: # try to create. If it fails, it must already exist
        qc.create_queue()
    except:
        pass
    qc.send_message(json.dumps(msg))

msg = prepare()
send(msg)