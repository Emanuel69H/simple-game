"""Connect to server"""

from time import sleep



class Connect:
    def __init__(self):
        x = 1
        for _ in range(3):
            print("Connecting")
            sleep(1)
        print("connected")
        # print("Connecting")

def start_connection():
    Connect()