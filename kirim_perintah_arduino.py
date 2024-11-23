import serial




serial_port = 'COM12'
baud_rate = 9600

try:
    ser = serial.Serial(serial_port, baud_rate)
except:
    print("PERIKSA NAMA COM ")

    
def send_command_to_arduino(status):
    """
    Mengirim perintah status ke Arduino melalui serial.
    """
    try:
        ser.write(str(status).encode())
        print("Mengirim perintah ke Arduino")
    except Exception as e:
        print("Gagal mengirim perintah ke Arduino:", e)