import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import requests
import subprocess
import time
import platform

system_type = platform.system()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 480)
        self.initUI()
        self.docker_process = None
        self.start_flask_api()
        self.dockerCommand=None

    def initUI(self):
        self.setWindowTitle('PyQt5 and Flask API')

        layout = QVBoxLayout()

        self.label = QLabel('Hello, World!', self)
        layout.addWidget(self.label)

        btn = QPushButton('Get Data from API', self)
        btn.clicked.connect(self.getData)
        layout.addWidget(btn)

        self.setLayout(layout)

        self.show()

    def wait_for_flask_api(self, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get('http://localhost:5000/')
                if response.status_code == 200:
                    return True
            except requests.exceptions.ConnectionError:
                time.sleep(1)
        return False

    def start_flask_api(self):
        if system_type == 'Linux':
            self.dockerCommand = ['sudo','docker', 'compose', 'up', '--build']
        else:
            self.dockerCommand = ['docker', 'compose', 'up', '--build']
        self.docker_process = subprocess.Popen(
            self.dockerCommand, # 前面加sudo用於linux
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if not self.wait_for_flask_api():
            print("Failed to start Flask API")

    def stop_flask_api(self):
        # if self.docker_process:
        #     self.docker_process.terminate()
        #     self.docker_process.wait()
        if system_type == 'Linux':
            self.dockerCommand = ['sudo', 'docker','compose', 'stop']
        else:
            self.dockerCommand = ['docker','compose', 'stop']
        subprocess.run(self.dockerCommand) # 前面加sudo用於linux
    

    def getData(self):
        response = requests.get('http://localhost:5000/')
        if response.status_code == 200:
            data = response.json()
            self.label.setText(data.get(data['Sentrak']))

    def closeEvent(self, event):
        self.stop_flask_api()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
