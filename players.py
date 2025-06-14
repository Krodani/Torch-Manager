from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import glob

class Player(QMainWindow):

    def player_manager(self):

        if glob.glob("usercache.json") and glob.glob("ops.json") and glob.glob("whitelist.json") and glob.glob("banned-players.json") and glob.glob("banned-ips.json"):

            # Get data from files and save to manipule

            bannedP = open(self.dir_path + "\\banned-players.json","r")
            banPlayers = str(bannedP.readlines())
            bannedP.close()

            user = open(self.dir_path + "\\usercache.json","r")
            usercache = str(user.readlines())
            user.close()

            ops = open(self.dir_path + "\\ops.json","r")
            usersOps = str(ops.readlines())
            ops.close()

            whitelistJson = open(self.dir_path + "\\whitelist.json","r")
            whitelist = str(whitelistJson.readlines())
            whitelistJson.close()
        
            # UserCache

            clearText = usercache.translate({ord(i): None for i in "{['\"]}"})
            dataUserSplit = clearText.split(',')

            playerName=[]
            playerUuid=[]
            for i in range(0,len(dataUserSplit)):
                if dataUserSplit[i].startswith("name"):
                    userName = dataUserSplit[i].split(":")
                    playerName += [str(userName[1])]            # Name from players
                if dataUserSplit[i].startswith("uuid"):
                    userUuid = dataUserSplit[i].split(":")
                    playerUuid += [str(userUuid[1])]            # Uuid from players

            # Banned-Players

            clearText = banPlayers.translate({ord(i): None for i in "{[\" ',.]}"})
            banPlayersSplit = clearText.split("\\n")

            delete=[]
            for i in range(0,len(banPlayersSplit)):
                if banPlayersSplit[i] in '':
                    delete.append(i)
        
            delete.sort(reverse=True)
            for i in delete:
                banPlayersSplit.pop(i)

            # With after data extract only Uuid

            banUuid=[]
            for i in range(0,len(banPlayersSplit)):
                if banPlayersSplit[i].startswith("uuid"):
                    uuid = banPlayersSplit[i].split(":")
                    banUuid += [str(uuid[1])]

            # Ops
        
            clearText = usersOps.translate({ord(i): None for i in "{[\" ',.]}"})
            usersOpsSplit = clearText.split("\\n")

            delete=[]
            for i in range(0,len(usersOpsSplit)):
                if usersOpsSplit[i] in '':
                    delete.append(i)

            delete.sort(reverse=True)
            for i in delete:
                usersOpsSplit.pop(i)

            # With after data extract only Uuid

            OPuuid = []
            count = 0
            while(True):
                if len(usersOpsSplit) > count:
                    OPuuid += usersOpsSplit[count].split("uuid:")
                    OPuuid.remove("")
                    count += 4
                else:
                    break

            # WhiteList
        
            clearText = whitelist.translate({ord(i): None for i in "{[\" ',.]}"})
            whitelistSplit = clearText.split("\\n")

            delete=[]
            for i in range(0,len(whitelistSplit)):
                if whitelistSplit[i] in '':
                    delete.append(i)

            delete.sort(reverse=True)
            for i in delete:
                whitelistSplit.pop(i)
        
            # With after data extract only Uuid

            WLuuid = []
            count = 0
            while(True):
                if len(whitelistSplit) > count:
                    WLuuid += whitelistSplit[count].split("uuid:")
                    WLuuid.remove("")
                    count += 2
                else:
                    break

        # Compare the after Uuid extracted with list of players 

        #valueT= 0
        #tableWL= [None] * len(playerUuid)
        #restart = True

        #while(restart):
            #for i in range(0, len(playerUuid)):
                #try:
                    #if WLuuid[valueT] in playerUuid[i]:
                        #tableWL[i] = "✔"
                        #valueT += 1
                        #break

                #except:
                    #for i in range(0, len(tableWL)):
                        #if tableWL[i] == None:
                            #tableWL[i] = "✖"
                    #restart = False

        
        #playerName.sort()
        #playerUuid.sort()
            self.tablePlayers.setRowCount(0)
            for i in range(len(playerName)):
                self.tablePlayers.insertRow(i)
            
                self.tablePlayers.setItem(i,0, QTableWidgetItem(playerName[i])) # Name
                self.tablePlayers.setItem(i,1, QTableWidgetItem(playerUuid[i]))    # Uuid
                self.tablePlayers.setItem(i,2, QTableWidgetItem("False"))    # Op
                self.tablePlayers.setItem(i,3, QTableWidgetItem("✖"))    # Whitelist
                self.tablePlayers.setItem(i,4, QTableWidgetItem("No Ban"))    # Ban
                self.tablePlayers.setItem(i,5, QTableWidgetItem("???"))    # Online

                for x in range(len(OPuuid)):
                    if(playerUuid[i] == OPuuid[x]):
                        self.tablePlayers.setItem(i,2, QTableWidgetItem("True"))    # Op
                        break

                for x in range(len(WLuuid)):
                    if(playerUuid[i] == WLuuid[x]):
                        self.tablePlayers.setItem(i,3, QTableWidgetItem("✔"))    # Whitelist
                        break

                for x in range(len(banUuid)):
                    if(playerUuid[i] == banUuid[x]):
                        self.tablePlayers.setItem(i,4, QTableWidgetItem("Banned"))    # Ban
                        break