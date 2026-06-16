import time
import serial
import serial.tools.list_ports

class Pico():
    def __init__(self):
        ports = serial.tools.list_ports.comports()
        if not ports:
            print("No serial devices found.")
            return
        time.sleep(15)
        for port in ports:
            if "USB Serial Device" in port.description:
                self.port = port.device
                break
        self.ser = serial.Serial(self.port, 115200, timeout=None)

    def Listen(self):
        #Listen for serial
        print("Started listening to serial for pico")
        time.sleep(1)
        UUID = self.ser.readline().decode('utf-8').strip()
        return UUID
    
    def Open(self, tim):
        if tim > 0:
            self.ser.write((f"200 OK;{tim}\n").encode('utf-8'))
        else:
            self.ser.write((f"401 Denied;-1\n").encode('utf-8'))

    