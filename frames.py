import glob, os
from PyQt5 import QtMultimedia
from PyQt5.QtWidgets import QMainWindow
from about import About
from players import Player

class Frame(QMainWindow):
    menu = None
    menu_about = False

    def sound_click():
        sound_path = os.path.join(os.path.dirname(__file__), "repository", "minecraft_click.wav")
        QtMultimedia.QSound.play(sound_path)

    def viewServer(self, event):
        if Frame.menu != "server":
            Frame.sound_click()
            Frame.hide_frames(self, "hide")
            self.serverFrame.show()
            Frame.menu = "server"

    def viewCommands(self, event):
        if Frame.menu != "commands":
            Frame.sound_click()
            Frame.hide_frames(self, "hide")
            self.comandsFrame.show()
            Frame.menu = "commands"

    def viewInstall(self, event):
        if Frame.menu != "install":
            Frame.sound_click()
            Frame.hide_frames(self, "hide")
            self.installFrame.show()
            Frame.menu = "install"
 
    def viewPlayers(self, event):
        
        if Frame.menu != "players":
            Frame.sound_click()
            Frame.hide_frames(self, "hide")
            self.playersFrame.show()
            
            Player.player_manager(self)
            Frame.menu = "players"
 
    def viewAbout(self, event):
        
        if Frame.menu != "about":
            Frame.sound_click()
            self.reg = About()
            self.reg.show()
            Frame.menu = "about"
        
    def hide_frames(self, frame):

        if frame == "hide":
            self.serverFrame.hide()
            self.comandsFrame.hide()
            self.playersFrame.hide()
            self.installFrame.hide()
            self.serverAdbancedOptionsFrame.hide()
            self.serverAdbancedOptionsFrame_2.hide()
        else:
            #TODO add advanced options
            if frame == "ao1":
                Frame.hide_frames(self, "hide")
                self.serverAdbancedOptionsFrame.show()
            if frame == "ao2":
                Frame.hide_frames(self, "hide")
                self.serverAdbancedOptionsFrame_2.show()

    def showInstall(self):

        if self.pushButton_showInstall.text() == "Show more":
            self.pushButton_showInstall.setText("Hide")
            self.textEdit_install.show()

        else:
            self.pushButton_showInstall.setText("Show more")
            self.textEdit_install.hide()

    def print_jar(self):
        self.comboBox_selectServer.clear()
        
        for file in glob.glob("*.jar"):
            self.comboBox_selectServer.addItem(os.path.splitext(file)[0])  # Add items without .jar