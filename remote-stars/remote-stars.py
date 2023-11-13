import math
import socket
import numpy as np
from skimage.measure import label, regionprops

SERVER_ADDRESS = "84.237.21.36"
SERVER_PORT_ALT = 5152


def recvall(sock, bytes_count):
    data = bytearray()
    while len(data) < bytes_count:
        packet = sock.recv(bytes_count - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def process_image():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        beat = b'nope'
        sock.connect((SERVER_ADDRESS, SERVER_PORT_ALT))
        while beat != b'yep':
            sock.send(b"get")
            bts = recvall(sock, 40002)
            image = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0], bts[1])
            image[image > 1] = 1
            regions = regionprops(label(image))
            x_f, y_f = regions[0].centroid
            x_s, ys = regions[1].centroid
            distance = round(math.sqrt((x_s - x_f) ** 2 + (ys - y_f) ** 2), ndigits=1)
            sock.send(f"{distance}".encode())
            sock.send(b'beat')
            beat = sock.recv(20)
        print("DONE")


def main():
    process_image()


if __name__ == '__main__':
    main()
