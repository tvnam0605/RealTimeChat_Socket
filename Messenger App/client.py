import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QInputDialog

HOST = '127.0.0.1'
PORT = 1234

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tin nhắn')
        self.setGeometry(100, 100, 600, 600)
        self.setFixedSize(600, 600)

        self.layout = QVBoxLayout()

        self.message_box = QTextEdit(self)
        self.message_box.setReadOnly(True)
        self.layout.addWidget(self.message_box)

        self.bottom_layout = QHBoxLayout()

        self.message_textbox = QLineEdit(self)
        self.bottom_layout.addWidget(self.message_textbox)

        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_message)
        self.bottom_layout.addWidget(self.send_button)

        self.layout.addLayout(self.bottom_layout)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                font-size: 14px;
                border: 1px solid #ccc;
            }

            QLineEdit {
                background-color: #fff;
                font-size: 14px;
                border: 1px solid #ccc;
                padding: 4px;
            }

            QPushButton {
                background-color: #3498db;
                color: white;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px 10px;
            }

            QPushButton:hover {
                background-color: #2980b9;
                border: 2px solid #2980b9;
            }
        """)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        try:
            self.client.connect((HOST, PORT))  # Kết nối tới máy chủ qua địa chỉ và cổng
            self.add_message("[SERVER] Kết nối thành công với máy chủ")  
        except:
            self.add_message("Không thể kết nối tới máy chủ") 

        username, ok = QInputDialog.getText(self, "Nhập tên người dùng", "Tên người dùng:")  
        if ok and username:
            self.client.sendall(username.encode())  # Gửi tên người dùng tới server
        else:
            self.add_message("Tên người dùng không hợp lệ") 

        threading.Thread(target=self.listen_for_messages_from_server).start()  # Bắt đầu lắng nghe tin nhắn từ server trong một luồng riêng

    def send_message(self):
        message = self.message_textbox.text()  # Lấy nội dung tin nhắn từ hộp văn bản
        if message:
            self.client.sendall(message.encode())  # Gửi tin nhắn tới server
            self.message_textbox.clear()  # Xóa nội dung hộp văn bản sau khi gửi
        else:
            self.add_message("Tin nhắn không thể trống") 

    def add_message(self, message):
        self.message_box.append(message)  # Thêm tin nhắn vào hộp văn bản

    def listen_for_messages_from_server(self):
        while True:
            message = self.client.recv(2048).decode('utf-8') 
            if message:
                username = message.split("~")[0]  # Tách tên người dùng từ tin nhắn
                content = message.split('~')[1]  # Tách nội dung tin nhắn
                self.add_message(f"[{username}] {content}")  # Hiển thị tin nhắn với tên người dùng
            else:
                self.add_message("Tin nhắn nhận từ máy chủ trống rỗng") 

def main():
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
