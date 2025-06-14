import os, glob, subprocess
from PyQt5 import QtCore
from PyQt5.QtCore  import Qt
from PyQt5.QtWidgets import QMainWindow
from download import install, WorkerDownload
from settings import Settings
from frames import Frame

class ServerThread(QtCore.QThread):

    threadWorker = QtCore.pyqtSignal(str)
    is_running = False

    def __init__(self, parent=None, command= None):
        super(ServerThread, self).__init__(parent)
        self.command = command

    def run(self):

        self.process = subprocess.Popen(self.command, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

        for line in iter(self.process.stdout.readline, b''):
            line = line.decode('utf-8', errors='replace').strip()
            self.threadWorker.emit(line)

        self.process.wait()  # Wait for the process to finish completely
        self.quit()  # End of implementation

        
    def send_comand(self):
        
            enterComand = bytes(userCommand, 'utf-8')
            self.process.stdin.write(enterComand + b"\n")
            self.process.stdin.flush()
            #t = time.localtime()
            #print("[" + time.strftime("%H:%M:%S", t) + "] [Server comand/INPUT]: " + userCommand)


    def stop_server_command(self):

        try:
            self.process.stdin.write(b"stop\n")
            self.process.stdin.flush()
        
        except Exception as e:
            print(f"Error sending command: {e}")


class Server(QMainWindow):

    def on_start_check_java(self):

        pattern = install.java_path(self.comboBox_selectServer.currentText())
        java_num = install.java_version(self.comboBox_selectServer.currentText())

        if not self.serverStatus and not os.path.exists(pattern):
            only_java = "True"
            self.label_serverError.setText("Downloading Java, Wait")
        else:
            only_java = "None"



        self.JavaDownload = WorkerDownload(only_java, pattern, java_num)
        self.JavaDownload.finished.connect(lambda: Server.start_server(self))
        self.JavaDownload.start()
        
    def start_server(self):

        # Start server if there is no other server open if there is one then shut it down
        if not self.serverStatus:

            Server.manage_eula(self)

            Settings.save_properties(self)
            self.label_serverError.setText("")
            self.textEdit_Commands.clear()
            Frame.viewCommands(self, None)
            
            self.textEdit_Commands.setEnabled(True)
            self.lineEdit_Commands.setEnabled(True)
            self.pushButton_Commands.setEnabled(True)

            # Run Server

            sample_string = str(self.comboBox_selectServer.currentText())
            if sample_string.lower().startswith("forge"):
                char_to_replace = {"forge-1.": "", '.jar': ''}
                for key, value in char_to_replace.items():
                    sample_string = sample_string.replace(key, value)
                testsplit = sample_string.split("-")
                version = float(testsplit[0])

            java_path = install.java_path(self.comboBox_selectServer.currentText())

            if self.comboBox_selectServer.currentText().lower().startswith("forge") and version >= 17:
                command = f'"{java_path}" -Xmx{self.spinBox_Ram.value()}{self.comboBox_Ram.currentText()[0]} -Xms{self.spinBox_Ram.value()}{self.comboBox_Ram.currentText()[0]} @{self.comboBox_selectServer.currentText()}.jar nogui %*'
            else:
                command = f'"{java_path}" -Xmx{self.spinBox_Ram.value()}{self.comboBox_Ram.currentText()[0]} -Xms{self.spinBox_Ram.value()}{self.comboBox_Ram.currentText()[0]} -jar {self.comboBox_selectServer.currentText()}.jar nogui'

            # Set server running
            self.serverStatus = True
            self.startServer.setText("Stop")

            # Call thread and start running server
            self.worker= ServerThread(None, command)
            self.worker.threadWorker.connect(self.textEdit_Commands.append)
            self.worker.finished.connect(lambda: Server.reset_instances(self))
            self.worker.start()

        else:
            self.worker.stop_server_command()
            self.serverStatus = False
            self.startServer.setText("Start")
            #self.textEdit_Commands.setEnabled(False)
            self.lineEdit_Commands.setEnabled(False)
            self.pushButton_Commands.setEnabled(False)


    def manage_eula(self):

        # if this file don't exist create a new eula.txt
        eula_path = "eula.txt"
        eula_status= False
        if not glob.glob(eula_path):
            Settings.eula_message(self)
        else:
            with open(eula_path, "r") as file:
                content = file.read()
                eula_status = "eula=false" in content

        if eula_status:
            Settings.eula_message(self)

    def reset_instances(self):
        self.serverStatus = False
        self.startServer.setText("Start")

    commandLoad = []
    posi = None
    maxi = None

    def send_comand_to_thread(self):

        if self.serverStatus == True:
            global userCommand
            userCommand = self.lineEdit_Commands.text()
            
            Server.commandLoad.append(userCommand)
            Server.posi = len(Server.commandLoad)
            Server.maxi = len(Server.commandLoad)
            

            self.lineEdit_Commands.setText("")
            self.worker.send_comand()

            if userCommand.lower() == "stop":
                self.worker.stop_server_command()
                self.serverStatus = False
                self.startServer.setText("Start")
        else:
            self.textEdit_Commands.setText("You need to start the server")
            self.lineEdit_Commands.setText("")

    def command_key_operation(self, event):
        try:
            key = event.key()
            
            if key == Qt.Key_Up and Server.posi > 0:
                Server.posi -= 1
                self.lineEdit_Commands.setText(Server.commandLoad[Server.posi])
            
            elif key == Qt.Key_Down and Server.posi < Server.maxi:
                Server.posi += 1
                self.lineEdit_Commands.setText(Server.commandLoad[Server.posi])
            
            elif key in (Qt.Key_Backspace, Qt.Key_Delete):
                self.lineEdit_Commands.setText(self.lineEdit_Commands.text()[:-1])
            
            elif key == Qt.Key_Return:
                Server.send_comand_to_thread(self)
            
            elif key not in (Qt.Key_Return, Qt.Key_Backspace, Qt.Key_Escape, Qt.Key_Delete):
                self.lineEdit_Commands.insert(event.text())

        except Exception as e:
            print(f"Error: {e}")

            
