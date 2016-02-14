import netifaces
import struct


def get_ip(version=4):
    """
    Returns the ip address of this computer
    """
    v = 2
    # if version == 4:
    #     v = netifaces.AF_INET
    # elif version == 6:
    #     v = netifaces.AF_INET6
    # else:
    #     raise ValueError("version should equal 4 or 6")

    for i in netifaces.interfaces():
        d = netifaces.ifaddresses(i)
        if v in d.keys():
            dd = d[v][0]
            if "broadcast" in dd.keys():
                # print i
                # print dd
                return dd["addr"]

def pack_ip(ip=None):
    if ip == None:
        ip == get_ip()
    parts = map(int, get_ip().split("."))
    out = struct.pack("!BBBB", parts[0], parts[1], parts[2], parts[3])
    return out

def unpack_ip(data):
    return ".".join(map(str, struct.unpack("!BBBB", data)))

if __name__ == '__main__':
    print get_ip()