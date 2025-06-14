from PyQt5.QtWidgets import QApplication, QMessageBox
import socket

class Settings(QApplication):

    def eula_message(self):

        reply = QMessageBox.question(self, "Eula conditions", "You accept the conditions of the eula?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            Settings.save_eula(self, "true")
        else:
            Settings.save_eula(self, "false")

    def save_eula(self, reply):

        eula = open(self.dir_path + "\\eula.txt","w")
        eula.write(
            "#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n"
            f"eula={reply}")
        
    def recource_pack_link_edit(self):

        #https://download722.mediafire.com/40mglj4bcrxg/ogoh7mpz1hkbbkq/1.16.5+Aluzion.zip
        link = self.lineEdit_RecourcePack.text()

        # List of characters to be modified
        split_character = [":", "=", "#"]

        for character in split_character:
            link = link.replace(character, "\\" + character)  # Agrega correctamente la barra invertida

        return link

    def save_properties(self):

        log2 = open(self.dir_path + "\\server.properties","w")
        log2.write(
            "#Minecraft server properties by Torch Manager\n"
            "#Wed Feb 03 16:17:56 CET 2021\n"
            "#ram=" + str(self.spinBox_Ram.value()) + ":" + str(self.comboBox_Ram.currentText()) + "\n"
            "enable-jmx-monitoring=" + str(self.checkBox_jmx.isChecked()).lower() + "\n"
            "rcon.port=" + str(self.spinBox_RconPort.value()) + "\n"
            "level-seed=" + str(self.lineEdit_Seed.text()) + "\n"
            "gamemode=" + str(self.comboBox_2.currentText()).lower() + "\n"
            "enable-command-block=" + str(self.checkBox_comandBlock.isChecked()).lower() + "\n"
            "enable-query=" + str(self.checkBox_Query.isChecked()).lower() + "\n"
            "generator-settings=\n"
            "level-name=" + str(self.lineEdit_7.text()) + "\n"
            "motd=" + str(self.lineEdit.text()) + "\n"
            "query.port=" + str(self.spinBox_QueryPort.value()) + "\n"
            "pvp=" + str(self.checkBox_pvp.isChecked()).lower() + "\n"
            "generate-structures=" + str(self.checkBox_structures.isChecked()).lower() + "\n"
            "difficulty=" + str(self.comboBox.currentText()).lower() + "\n"
            "network-compression-threshold=" + str(self.spinBox_NetworkCompression.value()) + "\n"
            "max-tick-time=" + str(self.spinBox_TickTime.value()) + "\n"
            "use-native-transport=" + str(self.checkBox_NativeTransport.isChecked()).lower() + "\n"
            "max-players=" + str(self.spinBox_Players.value()) + "\n"
            "online-mode=" + str(self.checkBox_online.isChecked()).lower() + "\n"
            "enable-status=" + str(self.checkBox_Status.isChecked()).lower() + "\n"
            "allow-flight=" + str(self.checkBox_flight.isChecked()).lower() + "\n"
            "broadcast-rcon-to-ops=" + str(self.checkBox_BroadcastRcon.isChecked()).lower() + "\n"
            "view-distance=" + str(self.spinBox_View.value()) + "\n"
            "max-build-height=" + str(self.spinBox_BuildHeight.value()) + "\n"
            "server-ip=" + str(self.lineEdit_Ip.text()) + "\n"
            "allow-nether=" + str(self.checkBox_nether.isChecked()).lower() + "\n"
            "server-port=" + str(self.spinBox_Port.value()) + "\n"
            "enable-rcon=" + str(self.checkBox_Rcon.isChecked()).lower() + "\n"
            "sync-chunk-writes=" + str(self.checkBox_SyncChunk.isChecked()).lower() + "\n"
            "op-permission-level=" + str(self.spinBox_OPLevel.value()) + "\n"
            "prevent-proxy-connections=" + str(self.checkBox_PreventProxy.isChecked()).lower() + "\n"
            "require-resource-pack=" + str(self.checkBox_EnableResourcePack.isChecked()).lower() + "\n"
            "resource-pack=" + str(Settings.recource_pack_link_edit(self)) + "\n"
            "entity-broadcast-range-percentage=" + str(self.spinBox_EntityRange.value()) + "\n"
            "rcon.password=" + str(self.lineEdit_RconPassword.text()) + "\n"
            "player-idle-timeout=0\n"
            "force-gamemode=" + str(self.checkBox_ForceGamemode.isChecked()).lower() + "\n"
            "rate-limit=0\n"
            "hardcore=" + str(self.checkBox_hardcore.isChecked()).lower() + "\n"
            "white-list=" + str(self.checkBox_WhiteList.isChecked()).lower() + "\n"
            "broadcast-console-to-ops=" + str(self.checkBox_BroadcastConsole.isChecked()).lower() + "\n"
            "spawn-npcs=" + str(self.checkBox_npcs.isChecked()).lower() + "\n"
            "spawn-animals=" + str(self.checkBox_animals.isChecked()).lower() + "\n"
            "snooper-enabled=" + str(self.checkBox_Snooper.isChecked()).lower() + "\n"
            "function-permission-level=" + str(self.spinBox_FunctionLevel.value()) + "\n"
            "level-type=" + str(self.lineEdit_Type.text()) + "\n"
            "text-filtering-config=\n"
            "spawn-monsters=" + str(self.checkBox_monsters.isChecked()).lower() + "\n"
            "enforce-whitelist=" + str(self.checkBox_EnforceWhitelist.isChecked()).lower() + "\n"
            "resource-pack-sha1=" + str(self.lineEdit_RecourcePackSh1.text()) + "\n"
            "spawn-protection=" + str(self.spinBox_SpawnProtection.value()) + "\n"
            "max-world-size=" + str(self.spinBox_WorldSize.value()) + "\n")
        log2.close()
        self.changeProprites = False

    def open_properties(self, dir_path):

        log = open(dir_path + "\\server.properties","r")
        txt = log.readlines()
        log.close()
        
        for i in range(2,len(txt)):

            if ("enable-command-block=true" or "enable-command-block=True") in txt[i]:
                self.checkBox_comandBlock.setChecked(True)
            if ("allow-flight=true" or "allow-flight=True") in txt[i]:
                self.checkBox_flight.setChecked(True)
            if ("allow-nether=true" or "allow-nether=True") in txt[i]:
                self.checkBox_nether.setChecked(True)
            if ("generate-structures=true" or "generate-structures=True") in txt[i]:
                self.checkBox_structures.setChecked(True)
            if ("hardcore=true" or "hardcore=True") in txt[i]:
                self.checkBox_hardcore.setChecked(True)
            if ("online-mode=true" or "online-mode=True") in txt[i]:
                self.checkBox_online.setChecked(True)
            if ("pvp=true" or "pvp=True") in txt[i]:
                self.checkBox_pvp.setChecked(True)
            if ("spawn-animals=true" or "spawn-animals=True") in txt[i]:
                self.checkBox_animals.setChecked(True)
            if ("spawn-monsters=true" or "spawn-monsters=True") in txt[i]:
                self.checkBox_monsters.setChecked(True)
            if ("spawn-npcs=true" or "spawn-npcs=True") in txt[i]:
                self.checkBox_npcs.setChecked(True)
            if ("white-list=true" or "white-list=True") in txt[i]:
                self.checkBox_WhiteList.setChecked(True)
            if ("force-gamemode=true" or "force-gamemode=True") in txt[i]:
                self.checkBox_ForceGamemode.setChecked(True)
            if ("snooper-enabled=true" or "snooper-enabled=True") in txt[i]:
                self.checkBox_Snooper.setChecked(True)
            if ("enable-jmx-monitoring=true" or "enable-jmx-monitoring=True") in txt[i]:
                self.checkBox_jmx.setChecked(True)
            if ("enable-status=true" or "enable-status=True") in txt[i]:
                self.checkBox_Status.setChecked(True)
            if ("enable-query=true" or "enable-query=True") in txt[i]:
                self.checkBox_Query.setChecked(True)
            if ("enable-rcon=true" or "enable-rcon=True") in txt[i]:
                self.checkBox_Rcon.setChecked(True)
            if ("prevent-proxy-connections=true" or "prevent-proxy-connections=True") in txt[i]:
                self.checkBox_PreventProxy.setChecked(True)
            if ("broadcast-rcon-to-ops=true" or "broadcast-rcon-to-ops=True") in txt[i]:
                self.checkBox_BroadcastRcon.setChecked(True)
            if ("broadcast-console-to-ops=true" or "broadcast-console-to-ops=True") in txt[i]:
                self.checkBox_BroadcastConsole.setChecked(True)
            if ("use-native-transport=true" or "use-native-transport=True") in txt[i]:
                self.checkBox_NativeTransport.setChecked(True)
            if ("enforce-whitelist=true" or "enforce-whitelist=True") in txt[i]:
                self.checkBox_EnforceWhitelist.setChecked(True)
            if ("require-resource-pack=true" or "require-resource-pack=True") in txt[i]:
                self.checkBox_EnableResourcePack.setChecked(True)
            if ("sync-chunk-writes=true" or "sync-chunk-writes=True") in txt[i]:
                self.checkBox_SyncChunk.setChecked(True)

            if txt[i].startswith("#ram="):
                x = txt[i].split("=")
                ram = x[1].split(":")
                self.spinBox_Ram.setValue(int(ram[0]))

                unidad = ram[1].strip()  # Elimina cualquier espacio en blanco o caracteres de nueva línea
    
                if unidad == "GB":  # Comparación con el valor limpio
                    self.comboBox_Ram.setCurrentIndex(0)
                elif unidad == "MB":
                    self.comboBox_Ram.setCurrentIndex(1)
                
                #if ram[1] == "G\n":
                    #self.comboBox_Ram.setCurrentIndex(1)
                #else:
                   #self.comboBox_Ram.setCurrentIndex(0)

            # TODO set the split here

            if txt[i].startswith("view-distance"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_View.setValue(int(x[1]))
            if txt[i].startswith("max-players"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_Players.setValue(int(x[1]))
            if txt[i].startswith("spawn-protection"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_SpawnProtection.setValue(int(x[1]))
            if txt[i].startswith("server-port"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_Port.setValue(int(x[1]))
            if txt[i].startswith("op-permission-level"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_OPLevel.setValue(int(x[1]))
            if txt[i].startswith("function-permission-level"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_FunctionLevel.setValue(int(x[1]))
            if txt[i].startswith("rcon.port"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_RconPort.setValue(int(x[1]))
            if txt[i].startswith("query.port"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_QueryPort.setValue(int(x[1]))
            if txt[i].startswith("network-compression-threshold"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_NetworkCompression.setValue(int(x[1]))
            if txt[i].startswith("entity-broadcast-range-percentage"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_EntityRange.setValue(int(x[1]))
            if txt[i].startswith("max-world-size"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_WorldSize.setValue(int(x[1]))
            if txt[i].startswith("max-tick-time"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_TickTime.setValue(int(x[1]))
            if txt[i].startswith("max-build-height"):
                x = txt[i].split("=")
                #hola = x[1].split("\n")
                self.spinBox_BuildHeight.setValue(int(x[1]))

            if txt[i].startswith("server-ip"):
                x = txt[i].split("=")
                ip = x[1].split("\n")
                if ip[0] == "":
                    hostname = socket.gethostname()
                    IPAddr = socket.gethostbyname(hostname)
                    self.lineEdit_Ip.setText(IPAddr)
                else:
                    self.lineEdit_Ip.setText(ip[0])

            # TODO Check \n in ends line
            if txt[i].startswith("difficulty"):
                x = txt[i].split("=")
                difficulty = {'Peaceful\n':0, 'Easy\n':1, 'Normal\n':2, 'Hard\n':3}
                for c, v in difficulty.items():
                    if  x[1] == c.lower():
                        self.comboBox.setCurrentIndex(v)
            if txt[i].startswith("gamemode"):
                x = txt[i].split("=")
                gamemode = {'Survival\n':0, 'Creative\n':1, 'Adventure\n':2, 'Spectator\n':3}
                for c, v in gamemode.items():
                    if  x[1] == c.lower():
                        self.comboBox_2.setCurrentIndex(v)


            if txt[i].startswith("motd"):
                x = txt[i].split("=")
                text = x[1].split("\n")
                self.lineEdit.setText(text[0])
            if txt[i].startswith("level-name"):
                x = txt[i].split("=")
                text = x[1].split("\n")
                self.lineEdit_7.setText(text[0])
            if txt[i].startswith("level-seed"):
                x = txt[i].split("=")
                text = x[1].split("\n")
                self.lineEdit_Seed.setText(text[0])
            if txt[i].startswith("level-type"):
                x = txt[i].split("=")
                text = x[1].split("\n")
                self.lineEdit_Type.setText(text[0])
            if txt[i].startswith("rcon.password"):
                x = txt[i].split("=")
                text = x[1].split("\n")
                self.lineEdit_RconPassword.setText(text[0])
            if txt[i].startswith("resource-pack="):
                
                x = txt[i].split("resource-pack=")
                text = x[1].split("\n")

                text[0] = text[0].replace("\\:", ":")
                text[0] = text[0].replace("\\=", "=")
                text[0] = text[0].replace("\\#", "#")

                self.lineEdit_RecourcePack.setText(text[0])

            if txt[i].startswith("resource-pack-sha1"):
                x = txt[i].split("=")
                text = x[1].split("\n")
                self.lineEdit_RecourcePackSh1.setText(text[0])