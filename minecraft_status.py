import socket
import struct
import json

def unpack_varint(s):
    d = 0
    for i in range(5):
        b = ord(s.recv(1))
        d |= (b & 0x7F) << 7*i
        if not b & 0x80:
            break
    return d

def pack_varint(d):
    o = b""
    while True:
        b = d & 0x7F
        d >>= 7
        o += struct.pack("B", b | (0x80 if d > 0 else 0))
        if d == 0:
            break
    return o

def pack_data(d):
    h = pack_varint(len(d))
    if type(d) == str:
        d = bytes(d, "utf-8")
    return h + d

def pack_port(i):
    return struct.pack('>H', i)

def get_info(host='localhost', port=25565):

    try:
    # Connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

    # Send handshake + status request
        s.send(pack_data(b"\x00\x00" + pack_data(host.encode('utf8')) + pack_port(port) + b"\x01"))
        s.send(pack_data("\x00"))

    # Read response
        unpack_varint(s)     # Packet length
        unpack_varint(s)     # Packet ID
        l = unpack_varint(s) # String length

        d = b""
        while len(d) < l:
            d += s.recv(1024)

    # Close our socket
        s.close()
        return json.loads(d.decode('utf8'))
    except:
        return None


    # Load json and return
