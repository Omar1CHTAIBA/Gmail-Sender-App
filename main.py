import smtplib
import ssl
from email.message import EmailMessage
import re
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton, QLineEdit, QLabel, QStackedWidget, QFileDialog, QMessageBox, QGridLayout

data = []

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initSettings()
        self.initUI()
        self.send.clicked.connect(self.send_email)
        self.add_attachment_button.clicked.connect(self.add_attachment)
        self.remove_attachment_button.clicked.connect(self.remove_attachment)
        self.attachments = []

    def initSettings(self):
        self.setWindowTitle("Gmail Sender")
        self.setGeometry(450, 150, 1000, 800)

    def initUI(self):
        # Create main widgets
        self.title = QLabel("Gmail Sender")
        self.title.setStyleSheet("font-size: 48px; font-weight: bold; color: #2196F3; text-align: center;")

        self.subject = QTextEdit()
        self.subject.setPlaceholderText("Subject")
        self.subject.setFixedHeight(100)
        self.subject.setStyleSheet("""
            QTextEdit {
                border: 2px solid #2980B9;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                background-color: #ECF0F1;
                color: #2C3E50;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }
            QTextEdit:focus {
                border: 2px solid #3498DB;
            }
        """)

        self.subject_label = QLabel("Subject")
        self.subject_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3;")

        self.body = QTextEdit()
        self.body.setPlaceholderText("Message")
        self.body.setMinimumHeight(500)
        self.body.setStyleSheet("""
            QTextEdit {
                border: 2px solid #3498DB;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                background-color: #ECF0F1;
                color: #2C3E50;
            }
            QTextEdit:focus {
                border: 2px solid #2980B9;
            }
        """)

        self.body_label = QLabel("Body")
        self.body_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3;")

        # Create attachment section widgets
        self.add_attachment_list = QTextEdit()
        self.add_attachment_list.setReadOnly(True)
        self.add_attachment_list.setMaximumWidth(200)
        self.add_attachment_list.setStyleSheet("""
            QTextEdit {
                background-color: #f1f1f1;
                color: #333;
                border: 2px solid #2196F3;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        self.add_attachment_button = QPushButton("Add Attachment")
        self.add_attachment_button.setFixedWidth(200)
        self.add_attachment_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-size: 14px;
                padding: 10px 10px;
                border: none;
                border-radius: 15px;
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background-color: #2980B9;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #1F618D;
            }
        """)

        self.remove_attachment_button = QPushButton("Remove Attachment")
        self.remove_attachment_button.setFixedWidth(200)
        self.remove_attachment_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                font-size: 14px;
                padding: 10px 10px;
                border: none;
                border-radius: 15px;
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background-color: #C0392B;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #A93226;
            }
        """)

        self.send = QPushButton("Send")
        self.send.setFixedWidth(700)
        self.send.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 22px;
                padding: 15px 30px;
                border: none;
                border-radius: 25px;
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background-color: #1976D2;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)

        self.html_edit_list = QTextEdit()
        self.html_edit_list.setReadOnly(False)
        self.html_edit_list.setMaximumWidth(200)
        self.html_edit_list.setStyleSheet("""
            QTextEdit {
                border: 2px solid #3498DB;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                background-color: #ECF0F1;
                color: #2C3E50;
            }
            QTextEdit:focus {
                border: 2px solid #2980B9;
            }
        """)

        # Create main layout
        self.layout = QHBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 20, 30, 20)

        # Create HTML editor layout
        html_layout = QVBoxLayout()
        html_layout.addWidget(self.html_edit_list)

        # Create middle layout for email components
        middle_layout = QVBoxLayout()
        middle_layout.setSpacing(20)
        middle_layout.setContentsMargins(50, 20, 50, 20)

        middle_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        middle_layout.addWidget(self.subject_label)
        middle_layout.addWidget(self.subject)
        middle_layout.addWidget(self.body_label)
        middle_layout.addWidget(self.body)
        middle_layout.addWidget(self.send, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create right side layout for attachments
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.add_attachment_list)
        right_layout.addWidget(self.add_attachment_button, alignment=Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.remove_attachment_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add all layouts to main layout
        self.layout.addLayout(html_layout)
        self.layout.addLayout(middle_layout)
        self.layout.addLayout(right_layout)

        # Set the layout
        self.setLayout(self.layout)

    def path_algorithm(self, path):
        if len(path) == 1:
            return path
        if path[-1] in ['\\', '/']:
            return ""
        else:
            return path[-1] + self.path_algorithm(path[:-1])

    def reverse_path_output(self, path):
        return path[::-1]

    def add_attachment(self):
        attachment_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if attachment_path:
            self.attachments.append(attachment_path)
            self.update_attachment_list()

    def remove_attachment(self):
        if self.attachments:
            self.attachments.pop()
            self.update_attachment_list()

    def update_attachment_list(self):
        attachment_text = ""
        for path in self.attachments:
            filename = path.split("/")[-1]  # Get the filename
            attachment_text += f"{filename}\n"
        self.add_attachment_list.setText(attachment_text)

    def send_email(self):
        subject = self.subject.toPlainText()
        body = self.body.toPlainText()
        html_content = self.html_edit_list.toPlainText()

        if subject and (body or html_content):
            self.subject.clear()
            self.body.clear()
            self.html_edit_list.clear()
            self.add_attachment_list.clear()

            try:
                smtp_server = "smtp.gmail.com"
                port = 587
                sender_email = data[1]
                password = data[2]

                msg = EmailMessage()
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = data[0]

                # Add HTML content if available
                if html_content:
                    msg.add_alternative(html_content, subtype='html')
                else:
                    msg.set_content(body)

                # Attach files if there are any
                if self.attachments:
                    for attachment in self.attachments:
                        with open(attachment, 'rb') as f:
                            file_data = f.read()
                            file_name = self.reverse_path_output(self.path_algorithm(attachment))
                            msg.add_attachment(file_data, maintype='application', subtype='octet-stream',
                                               filename=file_name)

                # Establish SSL connection and send email
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    server.starttls(context=context)
                    server.login(sender_email, password)
                    server.send_message(msg)

                # Clear attachments after sending email
                self.attachments.clear()

            except Exception as e:
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Icon.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText(f"An error occurred while sending the email: {str(e)}")
                error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                error_msg.exec()
        else:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.setWindowTitle("Error")
            error_msg.setText("Subject and body are required fields.")
            error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_msg.exec()



class InformationPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.email_pattern = r"^[A-z0-9\.]+@[A-z0-9]+\.(com|net|org|info)$"
        self.stacked_widget = stacked_widget
        self.setStyleSheet(""" /* Application-wide or InformationPage-wide stylesheet */
                    QLabel {
                        font-size: 56px;
                        font-weight: bold;
                        color: #2196F3;
                        text-align: center;
                    }
                    QLineEdit {
                        padding: 10px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                    }
                    QLineEdit:hover {
                        border: 1px solid #2196F3;
                    }
                    QLineEdit::placeholder {
                        color: #A0A0A0;
                    }
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        padding: 12px;
                        border: none;
                        border-radius: 8px;
                        font-size: 18px;
                        cursor: pointer;
                    }
                    QPushButton:hover {
                        background-color: #1976D2; /* Darker shade of blue on hover */
                    }

                """)
        self.initSettings()
        self.initUI()
        self.admit.clicked.connect(self.admit_logic)

    def initSettings(self):
        self.stacked_widget.setWindowTitle("Information Page")
        self.stacked_widget.setGeometry(450, 150, 1000, 800)

    def initUI(self):
        self.title = QLabel("Information Page")
        # self.title.setStyleSheet("font-size: 56px; font-weight: bold; color: #2196F3; text-align: center;")

        self.receiver_email = QLineEdit()
        self.receiver_email.setPlaceholderText("Enter recipient's email address")
        self.set_placeholder_color(self.receiver_email, "#2196F3")


        self.sender_email = QLineEdit()
        self.sender_email.setPlaceholderText("Enter your email address")
        self.set_placeholder_color(self.sender_email, "#2196F3")

        self.sender_password = QLineEdit()
        self.sender_password.setPlaceholderText("Enter your email password")
        self.sender_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.set_placeholder_color(self.sender_password, "#2196F3")


        self.html_edit = QTextEdit()
        self.html_edit.setPlaceholderText("Enter HTML content (optional)")
        self.html_edit.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px;")

        self.admit = QPushButton("Admit")
        self.admit.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                font-size: 22px;
                padding: 15px 30px;
                border: none;
                border-radius: 25px;
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background-color: #357ABD;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #2C6DAA;
            }
        """)
        self.admit.setFixedWidth(700)
        self.admit.setToolTip("Click to proceed with the email setup")

        self.layout = QGridLayout()  # Changed to QGridLayout
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(50, 20, 50, 20)

        # Add widgets to the grid layout
        self.layout.addWidget(self.title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.receiver_email, 1, 0, 1, 2)
        self.layout.addWidget(self.sender_email, 2, 0, 1, 2)
        self.layout.addWidget(self.sender_password, 3, 0, 1, 2)
        self.layout.addWidget(self.admit, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def set_placeholder_color(self, line_edit, color):
        placeholder_text = line_edit.placeholderText()
        line_edit.setStyleSheet(f"QLineEdit {{ color: {color};}}")
        line_edit.setPlaceholderText(placeholder_text)

    def admit_logic(self):
        receiver_email = self.receiver_email.text().strip()
        sender_email = self.sender_email.text().strip()
        sender_password = self.sender_password.text()

        if receiver_email and sender_email and sender_password:
            if re.match(self.email_pattern, receiver_email) and re.match(self.email_pattern, sender_email):
                data.append(receiver_email)
                data.append(sender_email)
                data.append(sender_password)
                self.stacked_widget.setCurrentIndex(1)
            else:
                self.receiver_email.setPlaceholderText("Not valid email address")
                self.sender_email.setPlaceholderText("Not valid email address")
        else:

            self.receiver_email.setPlaceholderText("Please fill in all fields.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wrapper = QStackedWidget()

    Info_window = InformationPage(wrapper)
    Main_window = MainWindow()

    wrapper.addWidget(Info_window)
    wrapper.addWidget(Main_window)

    wrapper.setCurrentIndex(0)

    wrapper.show()
    app.exec()
