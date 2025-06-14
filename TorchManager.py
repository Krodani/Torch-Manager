import threading
import sys, os, glob, urllib.request, json, webbrowser
from PyQt5.QtWidgets import QLineEdit, QSpinBox, QCheckBox, QComboBox, QFileDialog, QMessageBox
from PyQt5 import QtCore, QtWidgets, uic
from download import install
from frames import Frame
from settings import Settings
from server import Server

###################### add in start.exe gui file ############################
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

form = resource_path("TorchManager.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(form)
#############################################################################

class startAplication(QtWidgets.QMainWindow):
    
    serverStatus = False
    process = None
    public_ip_bool = True
    public_ip = None

    if getattr(sys, 'frozen', False):  # Si está ejecutándose como .exe con PyInstaller
        dir_path = os.path.dirname(sys.executable)  # Ruta del ejecutable
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))  # Ruta del script

    entercomand = QtCore.pyqtSignal(str)
    
    def __init__(self, parent = None):
        super(startAplication, self).__init__(parent)
        uic.loadUi(form, self)

        ########################## - Public IP - ##########################
        thread = threading.Thread(target=self.get_public_ip)
        thread.start()

        # Show Public ip when click
        self.lineEdit_publicIP.mousePressEvent = self.on_click_show_ip
        ###################################################################


        ################################ - Manage Frames - ##############################################

        # Shows which frame to display at application startup.
        startAplication.default_frame(self)

        self.label_Server.mousePressEvent = lambda event: Frame.viewServer(self, event)
        self.label_Commands.mousePressEvent = lambda event: Frame.viewCommands(self, event)
        self.label_Install.mousePressEvent = lambda event: Frame.viewInstall(self, event)
        self.label_Players.mousePressEvent = lambda event: Frame.viewPlayers(self, event)
        self.label_About.mousePressEvent = lambda event: Frame.viewAbout(self, event)

        # Show advanced options page 1 when click in advanced options
        self.advancedOptions.clicked.connect(lambda: Frame.hide_frames(self, "ao1"))
        # Back to server frame when click in back in advanced options page 1
        self.pushButton_AOBack.clicked.connect(lambda event: Frame.viewServer(self, event))
        # Show advanced options page 2 when click next in advanced options page 1
        self.pushButton_AONext.clicked.connect(lambda: Frame.hide_frames(self, "ao2"))
        # Back to advandec option page 1 when click back in page 2
        self.pushButton_AOBack_2.clicked.connect(lambda: Frame.hide_frames(self, "ao1"))
        # Hides the text window of the install tab and clicking the button causes it to show or hide.
        self.textEdit_install.hide()
        self.pushButton_showInstall.clicked.connect(lambda: Frame.showInstall(self))

        #################################################################################################
        
        ############ -- Server Frame -- ############

        # Set in lineEdit 3 and 4 the actucal path
        self.lineEdit_3.setText(self.dir_path)
        self.lineEdit_4.setText(self.dir_path) 

        # If this file exists compare with server.properties if it does not exist create a new server.properties
        if glob.glob("server.properties"):
            Settings.open_properties(self, self.dir_path)
        else:
            Settings.save_properties(self)

        # When you change a setting in the server configuration it registers that you have made a change.
        self.settings_changed()

        # Execute server when click button
        self.startServer.clicked.connect(lambda: Server.on_start_check_java(self))

        # GB to MB conversion and the other way around
        self.comboBox_Ram.currentIndexChanged.connect(self.transform_ram)

        # Save Settings in server.properties
        self.saveSetings.clicked.connect(lambda: Settings.save_properties(self))

        # Open select folder
        self.toolButton.clicked.connect(self.open_file_names_dialog)
        

        ############ -- Comands Frame -- ############

        # Enter comand to console
        self.pushButton_Commands.clicked.connect(lambda: Server.send_comand_to_thread(self))
        self.lineEdit_Commands.keyPressEvent = self.key_press_event

        # Open wiki of comands
        self.pushButton_Wiki.clicked.connect(lambda: webbrowser.open("https://minecraft.fandom.com/wiki/Commands#List_and_summary_of_commands"))


        ############ -- Install Frame -- ############

        # On select server print version for this
        self.comboBox_server.currentTextChanged.connect(lambda: install.print_versions_to_install(self))

        # When click buton openFileNamesDialog for select path to install 
        self.toolButton_2.clicked.connect(self.open_file_names_dialog)

        # When I click on the button, it downloads the server.
        self.pushButton_install.clicked.connect(lambda: install.get_data_to_download(self))
            

    def default_frame(self):
        
        # Get all names of .jar files in the current directory
        Frame.print_jar(self)

        # Hide all frames.
        Frame.hide_frames(self, "hide")
        
        # If there is a server in the current path show server frame, otherwise show installation frame
        if self.comboBox_selectServer.currentText() != "":
            self.serverFrame.show()
        else:  
            self.installFrame.show() 

    def on_click_show_ip(self, event):
            
            if self.public_ip_bool:
                self.lineEdit_publicIP.setText(self.public_ip)
                self.public_ip_bool = False
            else:
                self.lineEdit_publicIP.setText("**.**.**.**")
                self.public_ip_bool = True
            # Call the original event to maintain normal behaviour.
            QLineEdit.mousePressEvent(self.lineEdit_publicIP, event)

    def settings_changed(self):
        frames = ["serverFrame", "serverAdbancedOptionsFrame", "serverAdbancedOptionsFrame_2"]

        for frame_name in frames:
            frame = getattr(self, frame_name, None)  # Obtener el objeto QFrame
            if frame:
                for widget in frame.findChildren((QLineEdit, QSpinBox, QCheckBox, QComboBox)):
                    if widget.objectName() in ["comboBox_selectServer", "lineEdit_publicIP"]:
                        continue  # Saltar este widget para que no se conecte

                    if isinstance(widget, QLineEdit):
                        widget.textChanged.connect(lambda text, w=widget: self.change_detected(w))
                    elif isinstance(widget, QSpinBox):
                        widget.valueChanged.connect(lambda value, w=widget: self.change_detected(w))
                    elif isinstance(widget, QCheckBox):
                        widget.stateChanged.connect(lambda state, w=widget: self.change_detected(w))
                    elif isinstance(widget, QComboBox):
                        widget.currentIndexChanged.connect(lambda index, w=widget: self.change_detected(w))

    change_proprites = False
    def change_detected(self, widget):
        if not self.change_proprites:
            self.change_proprites = True
            #print(f"Cambio detectado en {widget.objectName()}")

    def key_press_event(self, event):
        Server.command_key_operation(self, event)

    def open_file_names_dialog(self):
        
        file = QFileDialog.getExistingDirectory(self,"Choose Directory")
        if file:
            self.lineEdit_3.setText(str(file))
            self.lineEdit_4.setText(str(file))

    def transform_ram(self):

        ram = self.spinBox_Ram.value()
        letter = self.comboBox_Ram.currentText()[0]

        conversion = {"G": 1 / 1024, "M": 1024}
        
        if letter in conversion:
            ram *= conversion[letter]
            self.spinBox_Ram.setMinimum(1 if letter == "G" else 1024)

        self.spinBox_Ram.setValue(int(ram))


    def get_public_ip(self): 
        
        try:
            # getting data
            with urllib.request.urlopen("https://api64.ipify.org?format=json") as response:
                data = json.loads(response.read().decode())  # Procesa la respuesta 
          
            # json data with key as origin 
            self.public_ip = data["ip"]
        except Exception as e:
            # if the website does not work it returns an error
            self.public_ip = "Error"

    def closeEvent(self, event):

        # If you try to close the application, the server is down and a change has been made to the properties settings, a message pops up to save the changes.
        if not self.serverStatus and self.change_proprites:
            reply = QMessageBox.question(self, "Exit", "You have left changes unsaved do you want to save them?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                Settings.save_properties(self)
            event.accept()

        # If the server is switched on, ask if you want to exit the application
        if self.serverStatus:
            reply = QMessageBox.question(self, "Exit", "The server is open, are you sure you want to close it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                #TODO Verificar que el servidor se cierra antes que el programa para evitar corrupcion de mundo
                Server.start_server(self)
                event.accept()
            else:
                event.ignore()

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    interfaceGui = startAplication()
    interfaceGui.show()
    app.exec_()