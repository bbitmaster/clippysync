import argparse
import yaml
import threading
import clipman
import socket
import psutil
import time

def load_config(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config

def send_clipboard(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            client_socket.sendall(data.encode())
        except ConnectionRefusedError:
            pass

def receive_clipboard(host, port, allowed_hosts):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        client_socket, address = server_socket.accept()
        if address[0] in allowed_hosts:
            data = b''
            while True:
                chunk = client_socket.recv(1048576)
                if not chunk:
                    break
                data += chunk
            clipman.set(data.decode())
        client_socket.close()


def get_ip_addresses():
    ip_addresses = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_addresses.append(addr.address)
    return ip_addresses

def waitForNewPaste(timeout=None):
    startTime = time.time()
    originalText = clipman.get()
    while True:
        currentText = clipman.get()
        if currentText != originalText:
            return currentText
        time.sleep(0.01)
        if timeout is not None and time.time() > startTime + timeout:
            raise TimeoutError('waitForNewPaste() timed out after ' + str(timeout) + ' seconds.')

def start_clipboard_sharing(config):
    ip_addresses = get_ip_addresses()
    if not ip_addresses:
        print("No network interfaces found.")
        return

    host = None
    port = None
    for ip_address in ip_addresses:
        if ip_address in config["machines"]:
            host = ip_address
            port = config["machines"][ip_address]
            break

    if host is None or port is None:
        print("No matching IP address found in the configuration.")
        return

    allowed_hosts = list(config["machines"].keys())
    receive_thread = threading.Thread(target=receive_clipboard, args=(host, port, allowed_hosts))
    receive_thread.start()

    last_clipboard = clipman.get()

    while True:
        try:
            current_clipboard = waitForNewPaste()
            if current_clipboard != last_clipboard:
                last_clipboard = current_clipboard
                for machine_host, machine_port in config["machines"].items():
                    if machine_host != host:
                        send_clipboard(machine_host, machine_port, current_clipboard)
        except clipman.exceptions.ClipmanBaseException as e:
            print("Clipman error:", e)

def main():
    parser = argparse.ArgumentParser(
        description='A tool for syncing clipboards across multiple machines',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument('--config', required=True, help='Path to the YAML configuration file')
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit\n\n'
                             'Example configuration file:\n'
                             '---\n'
                             'machines:\n'
                             '  192.168.0.10: 50000\n'
                             '  192.168.0.11: 50000\n')

    args = parser.parse_args()

    try:
        clipman.init()
        config = load_config(args.config)
        start_clipboard_sharing(config)
    except clipman.exceptions.ClipmanBaseException as e:
        print("Clipman error:", e)
    except FileNotFoundError:
        print(f"Configuration file not found: {args.config}")
    except yaml.YAMLError as e:
        print(f"Invalid YAML configuration: {e}")

if __name__ == "__main__":
    main()