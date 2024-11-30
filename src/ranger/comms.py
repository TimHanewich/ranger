import psutil

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