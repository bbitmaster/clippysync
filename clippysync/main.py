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
            print(f"Sent clipboard data to {host}:{port} ({len(data)} characters)")
        except ConnectionRefusedError:
            pass

def receive_clipboard(host, port, allowed_hosts, stop_event):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.settimeout(1.0)  # Set a timeout of 1 second

    while not stop_event.is_set():
        try:
            client_socket, address = server_socket.accept()
            client_socket.settimeout(1.0)  # Set a timeout of 1 second
            if address[0] in allowed_hosts:
                data = b''
                while True:
                    try:
                        chunk = client_socket.recv(1048576)
                        if not chunk:
                            break
                        data += chunk
                    except socket.timeout:
                        if stop_event.is_set():
                            break
                clipboard_data = data.decode()
                clipman.set(clipboard_data)
                print(f"Received clipboard data from {address[0]}:{address[1]} ({len(clipboard_data)} characters)")
            client_socket.close()
        except socket.timeout:
            pass

    server_socket.close()


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
        try:
            currentText = clipman.get()
            if currentText != originalText:
                return currentText
            time.sleep(0.01)
            if timeout is not None and time.time() > startTime + timeout:
                raise TimeoutError('waitForNewPaste() timed out after ' + str(timeout) + ' seconds.')
        except KeyboardInterrupt:
            raise

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
    stop_event = threading.Event()
    receive_thread = threading.Thread(target=receive_clipboard, args=(host, port, allowed_hosts, stop_event))
    receive_thread.start()

    last_clipboard = clipman.get()

    try:
        while not stop_event.is_set():
            try:
                current_clipboard = waitForNewPaste()
                if current_clipboard != last_clipboard:
                    last_clipboard = current_clipboard
                    for machine_host, machine_port in config["machines"].items():
                        if machine_host != host:
                            send_clipboard(machine_host, machine_port, current_clipboard)
            except clipman.exceptions.ClipmanBaseException as e:
                print("Clipman error:", e)
    except KeyboardInterrupt:
        print("\nExiting ClippySync...")
        stop_event.set()

    receive_thread.join()

def main():
    parser = argparse.ArgumentParser(
        description='A tool for syncing clipboards across multiple machines',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Example configuration file:\n'
               '---\n'
               'machines:\n'
               '  192.168.0.10: 50000\n'
               '  192.168.0.11: 50000\n'
    )
    parser.add_argument('--config', required=True, help='Path to the YAML configuration file')

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