
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 # Bạn có thể sử dụng ngẫu nhiên cổng từ 0 đến 65535
LISTENER_LIMIT = 5
active_clients = [] # Danh sách tất cả người dùng hiện đang kết nối

# Chức năng nghe tin nhắn sắp tới từ khách hàng
def listen_for_messages(client, username):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        else:
            print(f"Tin nhắn gửi từ client {username} trống")


# Chức năng gửi tin nhắn đến một khách hàng
def send_message_to_client(client, message):

    client.sendall(message.encode())

# Chức năng gửi bất kỳ tin nhắn mới nào tới tất cả khách hàng
# hiện đang được kết nối với máy chủ này
def send_messages_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

#Chức năng xử lý client
def client_handler(client):
    
# Máy chủ sẽ lắng nghe tin nhắn của khách hàng sẽ
    # Chứa tên người dùng
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} đã tham gia cuộc trò chuyện"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username trống")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# Chức năng chính
def main():

   # Tạo đối tượng lớp socket
    # AF_INET: chúng ta sẽ sử dụng địa chỉ IPv4
    # SOCK_STREAM: chúng tôi đang sử dụng các gói TCP để liên lạc
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Cung cấp cho máy chủ một địa chỉ dưới dạng
        # IP máy chủ và cổng
        server.bind((HOST, PORT))
        print(f"Đang chạy server trên {HOST} {PORT}")
    except:
        print(f"Không thể liên kết với máy chủ: {HOST} và cổng {PORT}")

# Đặt giới hạn máy chủ
    server.listen(LISTENER_LIMIT)

# Vòng lặp while này sẽ tiếp tục lắng nghe các kết nối của client
    while 1:

        client, address = server.accept()
        print(f"Thành công kết nối tới client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()