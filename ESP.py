from serial.serialutil import SerialException
from serial import Serial
from serial.tools.list_ports import comports
from ast import literal_eval

class ESP():
    def __init__(self, port_of_interests, baudrate=115200, timeout=1, **args) -> None:
        self.ser = Serial(port_of_interests[0], baudrate=baudrate, timeout=timeout, **args)
        self.soft_reboot()
        

    def write_file(self, code_filename, destination_filename):
        self.easy_edit_mode()
        self.ser.write(bytes(self.print_to_paste(code_filename, destination_filename), 'utf-8'))
        self.soft_reboot()

    def soft_reboot(self):
        self.ser.write(b"\x04")
        assert '>>>' in self.ser.readlines()[-1].decode('ascii')

    def import_os(self):
        self.ser.write(b"import os\r\n")
        assert '>>>' in self.ser.readlines()[-1].decode('ascii')

    def perform_ls(self):
        self.import_os()
        self.ser.write(b"os.listdir()\r\n")
        response = self.ser.readlines()
        file_list = literal_eval(response[1].decode('ascii'))
        print(file_list)
        assert '>>>' in response[-1].decode('ascii')

    def delete_file(self, filename):
        self.import_os()
        self.ser.write(bytes(f"os.remove('{filename}')\r\n", 'utf-8'))
        assert '>>>' in self.ser.readlines()[-1].decode('ascii')
        

    def easy_edit_mode(self):
        self.ser.write(b"\x05")
        assert '===' in self.ser.readlines()[-1].decode('ascii')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.ser.close()

    @staticmethod
    def print_to_paste(code_filename, destination_filename):
        with open(code_filename, 'r') as f:
            program_lines = f.read()
        return f"program_lines = '''{program_lines}''' \r\nwith open('{destination_filename}', 'w') as f:\r\n    f.write(program_lines)"

    @staticmethod
    def view_all_ports():
        ports = comports()
        for port, desc, hwid in ports:
            print(f"{port}: {desc}, {hwid}")

    @staticmethod
    def get_port_by_description(description):
        ports = comports()
        for port, desc, hwid in ports:
            if description in desc:
                return port, desc, hwid
            else:
                raise SerialException(f"The port associated with {description} is not found!")
    
if __name__ == '__main__':
    ESP.view_all_ports()
    port_of_interests = ESP.get_port_by_description('Silicon Labs')
    print(port_of_interests)
    with ESP(port_of_interests) as my:
        my.write_file('boot_original.py','xyz.py')
        my.soft_reboot()
        my.perform_ls()
        my.delete_file('xyz.py')
        my.perform_ls()
    
