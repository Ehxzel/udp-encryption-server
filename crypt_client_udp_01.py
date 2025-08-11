import socket

def main():
    host = '127.0.0.1'
    port = 8006

    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print("Client started...")

    try:
        server_addr = (host, port)
        while True:
            message = input("Enter command (ENCRYPT:<text>, DECRYPT:<base64>, TERMINATE): ")
            if not message:
                continue
            client_socket.sendto(message.encode("ascii"), server_addr)
            response, addr = client_socket.recvfrom(4096)
            print(f"Server response: {response.decode('ascii').strip()}\n")

            if message.strip().upper() == "TERMINATE":
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Socket closed")

if __name__ == '__main__':
    main()