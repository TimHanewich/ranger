import psutil
import settings
import json
import requests

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
    
    # construct body
    body:str = "<QueueMessage><MessageText>" + json.dumps(msg) + "</MessageText></QueueMessage>"

    # Make POST request
    headers = {"Content-Type": "application/xml"}
    response = requests.post(_infer_r2c_sas_url(), headers=headers, data=body)
    
    # handle code?
    if response.status_code != 201:
        raise Exception("POST request to Azure Queue Service to upload message returned status code '" + str(response.status_code) + "', not the successful '201 CREATED'!")

def _infer_r2c_sas_url() -> str:
    """Infers the correct SAS URL to POST new messages to (to send a new message), from the generic SAS URL we have in the settings."""
    ToReturn:str = settings.azure_queue_sas_url
    ToReturn = ToReturn.replace(".queue.core.windows.net/", ".queue.core.windows.net/r2c/messages")
    return ToReturn