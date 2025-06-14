import glob, os, re, shlex, shutil, subprocess, urllib.request, zipfile
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from frames import Frame

class WorkerDownload(QtCore.QThread):

    progressBar = QtCore.pyqtSignal(int)
    textOutput = QtCore.pyqtSignal(str)
    is_running = False

    def __init__(self, only_java, pattern, java_num, parent=None):
        super(WorkerDownload, self).__init__(parent)
        self.only_java = only_java
        self.java_num = java_num
        self.pattern = pattern


    def run(self):
        
        # Download only java when running a server when it is not installed on the frame install
        if self.only_java == "True":
            if not os.path.exists(self.pattern):
                WorkerDownload.download_java(self, self.java_num)  # Solo descarga si no lo tiene

        # Download all from frame install 
        elif self.only_java == "False":
            # Verificamos antes si Java ya está descargado
            if not os.path.exists(self.pattern):
                WorkerDownload.download_java(self, self.java_num)
            else:
                self.textOutput.emit("Java already downloaded, skipping.")

            self.textOutput.emit("Download starter from: " + www)
            if name_server == "Spigot":
                WorkerDownload.download_BuildTools(self)

            elif name_server == "Forge":
                WorkerDownload.forge_installer(self)

            elif name_server == "Minecraft java server":
                save_path = selected_path + "\\server-" + version_server + ".jar"
                urllib.request.urlretrieve(www, save_path, self.Handle_Progress)
        
        self.textOutput.emit("Download finished now you can start the server")
        
    # Download BuildTools requiered to download spigot
    def download_BuildTools(self):
        command = f"curl -o BuildTools.jar {www}"
        
        with subprocess.Popen(shlex.split(command), shell=False, cwd=selected_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as buildtools:
            for line in buildtools.stdout:
                self.textOutput.emit(line.strip())

        WorkerDownload.download_spigot(self)

    # Download spigot method
    def download_spigot(self):
        java = install.java_path(version_server)
        command = f"'{java}' -jar BuildTools.jar --rev {version_server}"
        
        with subprocess.Popen(shlex.split(command), shell=False, cwd=selected_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as spigot:
            for line in spigot.stdout:
                self.textOutput.emit(line.strip())

        WorkerDownload.delete_residual_files_spigot(self)

    # Download forge installer
    def forge_installer(self):
        
        save_path = selected_path + "\\forge-" + version_server + "-installer.jar"
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(www, headers=headers)

        with urllib.request.urlopen(req) as response:
            with open(save_path, "wb") as file:
                file.write(response.read())

        WorkerDownload.forge_download(self)

    def forge_download(self):

        # verifica si encuentra installer.jar en la rua actual
        installers = glob.glob(f"{selected_path}/*-installer.jar")
        if not installers:
            self.textOutput.emit("No installer found.")
            return
        
        # Preparamos el comando para la descarga
        file_name = installers[0].split("\\")[-1]
        java = install.java_path(version_server)
        command = f"'{java}' -jar {file_name} --installServer"

        # Ejecutar el comando de instalación de forge
        process = subprocess.Popen(shlex.split(command), shell=False, cwd=selected_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Leer la salida del proceso
        for line in iter(process.stdout.readline, b''):
            decoded_line = line.decode('utf8').strip()
            self.textOutput.emit(decoded_line)
            if not decoded_line:
                break
        
        # If the downloaded version is higher than 1.17, take the file and rename it to a different path.
        if WorkerDownload.compare_versions(version_server, "1.17"):
        
            pattern = os.path.join(selected_path, f"libraries\\net\\minecraftforge\\forge\\{version_server}*")
            matching_folders = glob.glob(pattern)

            original_file = f"{matching_folders[0]}\\win_args.txt"

            # Define new file path and file name
            new_file = f"{selected_path}\\forge-{version_server}.jar"
            shutil.move(original_file, new_file)


        WorkerDownload.delete_residual_files_forge(self, file_name)

    def compare_versions(version, version_referencia="1.17"):
        # Convert versions into lists of numbers
        version_download_lista = list(map(int, version.split(".")))
        version_referencia_lista = list(map(int, version_referencia.split(".")))

        # Compare versions element by element
        return version_download_lista >= version_referencia_lista

    #TODO Fix method
    def Handle_Progress(self, blocknum, blocksize, totalsize): 
  
        # calculation of the process
        readed_data = blocknum * blocksize 
  
        if totalsize > 0: 
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.emit(int(download_percentage))

    # Delete residual files when forge has finished downloading, except for libraries that are necessary for forge to work.
    def delete_residual_files_forge(self, file_name):

        forge_files = [file_name, "installer.log", f"minecraft_server.{version_server}.jar", "run.bat", "run.sh", "user_jvm_args.txt", "README.txt"]
        self.textOutput.emit("Deleting residual file")
        try:
            for f in forge_files:
                if os.path.isfile(selected_path + "/" + f):
                    os.remove(selected_path + "/" + f)

            # Search for files with pattern "*-shim.jar" and delete them
            shim_files = glob.glob(os.path.join(selected_path, "*-shim.jar"))
            for shim_file in shim_files:
                os.remove(shim_file)

            self.textOutput.emit("Successfully deleted files")

        except:
            self.textOutput.emit("Error deleting files")


    def delete_residual_files_spigot(self):
        self.textOutput.emit("Deleting residual files")

        try:
            # Define items to be deleted
            folders = ["BuildData", "Bukkit", "CraftBukkit", "Spigot", "work"]
            patterns = ["apache-maven-*", "PortableGit-*"]
            files = ["BuildTools.jar", "BuildTools.log.txt"]

            # Delete folders with adjusted permissions
            for folder in folders:
                remove_path = os.path.join(selected_path, folder)
                if os.path.exists(remove_path):
                    WorkerDownload.change_permissions_recursive(remove_path, 0o777)
                    shutil.rmtree(remove_path, ignore_errors=True)

            # Deleting files and directories with patterns
            for pattern in patterns:
                for path in glob.glob(os.path.join(selected_path, pattern)):
                    shutil.rmtree(path, ignore_errors=True)

            # Delete specific files
            for file_name in files:
                file_path = os.path.join(selected_path, file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)

            self.textOutput.emit("Successfully deleted files")

        except Exception as e:
            self.textOutput.emit(f"Error deleting files: {e}")

    # Add admin permision to directory for delete
    def change_permissions_recursive(path, mode):
        for root, dirs, files in os.walk(path, topdown=False):
                for name in dirs + files:
                    os.chmod(os.path.join(root, name), mode)

    def download_java(self, required_version):
        
        appdata = os.environ.get('LOCALAPPDATA')
        if not appdata:
            print("The environment variable “LOCALAPPDATA” is not set.")
        else:
            torch_manager_path = os.path.join(appdata, 'Torch Manager')
            java_path = os.path.join(torch_manager_path, 'Java')
            
            # Check if the ‘Java’ folder exists and, if not, create it (including Torch Manager if necessary).
            if not os.path.exists(java_path):
                os.makedirs(java_path)

            download_path = java_path + "\\OpenJDK.zip" # Path where the downloaded file will be saved
            extract_path = os.path.join(os.getcwd(), java_path)  # Destination folder for extraction

            java_urls = {
                21: "https://download.java.net/java/GA/jdk21.0.2/f2283984656d49d69e91c558476027ac/13/GPL/openjdk-21.0.2_windows-x64_bin.zip",
                17: "https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_windows-x64_bin.zip",
                16: "https://download.java.net/java/GA/jdk16.0.2/d4a915d82b4c4fbb9bde534da945d746/7/GPL/openjdk-16.0.2_windows-x64_bin.zip",
                11: "https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_windows-x64_bin.zip",
                8: "https://builds.openlogic.com/downloadJDK/openlogic-openjdk/8u422-b05/openlogic-openjdk-8u422-b05-windows-x64.zip"
            }
            
            url = java_urls[required_version]

            self.textOutput.emit(f"Downloading OpenJDK from {url}")
            urllib.request.urlretrieve(url, download_path)
            self.textOutput.emit(f"Download completed: {download_path}")
            WorkerDownload.extract_java(self, download_path, extract_path)


    def extract_java(self, zip_path, dest_folder):

        self.textOutput.emit(f"Unzipping {zip_path} to {dest_folder}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)
        self.textOutput.emit(f"Decompression completed.")

        WorkerDownload.delete_zip(self, zip_path)
        

    def delete_zip(self, zip_path):
        try:
            self.textOutput.emit(f"Deleting residual files.")
            os.remove(zip_path)
            self.textOutput.emit(f"File {zip_path} successfully deleted.")
        except Exception as e:
            self.textOutput.emit(f"File could not be deleted: {e}")

class install(QApplication):

    # when change server to download on install frame print versions for specific server
    def print_versions_to_install(self):
        selected_server = self.comboBox_server.currentText()
        if selected_server == " -- Select --":
            self.comboBox_version.clear()
            self.comboBox_version.addItem("None")
            return

        url = "https://gist.githubusercontent.com/Krodani/fa125faa09b7e31be2542512aeeb9dec/raw/0cb7098bb8960aad5782937c1506d714a878ce58/MCservers.txt"
        headers = {"User-Agent": "Mozilla/5.0"}

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode()

        servers = content.split("///")
        server_map = {
            "Minecraft java server": 1,
            "Mohist": 2,
            "Purpur": 3,
            "Forge": 5
        }

        self.comboBox_version.clear()

        if selected_server in server_map:
            version = servers[server_map[selected_server]].split("=")
            version.pop()
            for entry in version:
                html = entry.split("\n")
                self.comboBox_version.addItem(html[1])


        elif selected_server == "Spigot":
            version = servers[4].split("\n")[2:]  # We delete the first line which is the BuildTools link
            for entry in version:
                self.comboBox_version.addItem(entry)


    # Get all data for parse to download like server version name and url
    # TODO mirar version_download para quitar es la version que he sacado del pastebin con la ruta de descarga
    def get_data_to_download(self):

        self.textEdit_install.clear()

        name_server = self.comboBox_server.currentText()
        version_server = self.comboBox_version.currentText()

        gists_url = "https://gist.githubusercontent.com/Krodani/fa125faa09b7e31be2542512aeeb9dec/raw/483dd7fc38256084e4dfe6e9dd13d7b516d195ed/MCservers.txt" # URL de descarga
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            req = urllib.request.Request(gists_url, headers=headers)
            with urllib.request.urlopen(req) as response:
                pastebin = response.read().decode().split("///")  # Obtener y dividir contenido

        except Exception as e:
            self.label_InstallError.setText("Error al obtener datos: " + str(e))
            return

        servers_gists = {
            "Minecraft java server": 1,
            "Mohist": 2,
            "Purpur": 3,
            "Spigot": 4,
            "Forge": 5
        }

        if name_server not in servers_gists:
            self.label_InstallError.setText("Selecciona un servidor válido")
            return

        version_list = pastebin[servers_gists[name_server]].split("\n")[:-1]  # Eliminamos el último elemento vacío

        download_path_gists = version_list[1] if name_server == "Spigot" else next(
            (data.split("=")[1] for data in version_list if data.startswith(f"{version_server}=")), None
            )

        if download_path_gists:
            self.label_InstallError.setText("")
            install.server_download(self, name_server, download_path_gists)
        else:
            self.label_InstallError.setText("Versión no encontrada")


    def server_download(self, name_servers, download_path_gists): 
        
        global www, version_server, selected_path, name_server
        selected_path = self.lineEdit_4.text()
        version_server = self.comboBox_version.currentText()
        name_server = name_servers
        www = download_path_gists

        if selected_path != "":

            only_java = "False"
            pattern = install.java_path(self.comboBox_version.currentText())
            java_num = install.java_version(self.comboBox_version.currentText())

            self.WorkerDownload = WorkerDownload(only_java, pattern, java_num)        
            self.WorkerDownload.textOutput.connect(self.textEdit_install.append)
            self.WorkerDownload.progressBar.connect(self.progressBar.setValue)
            self.WorkerDownload.finished.connect(lambda: Frame.print_jar(self))
            self.WorkerDownload.start()            

        else:
            self.label_InstallError.setText("Insert path")
    
    # Take as imput value per example server-1.14.jar and this output is 1.14
    def extract_version(nombre_version):
        patron = r"\d+(\.\d+)*"
        resultado = re.search(patron, nombre_version)
        return resultado.group() if resultado else None

    def convert_version(version):
        partes = list(map(int, version.split(".")))
        while len(partes) < 3:  # Ensure it has three elements
            partes.append(0)
        return tuple(partes)

    def java_version(server_version):

        try:
            server_version = install.extract_version(server_version)
            server_version = install.convert_version(server_version)

            if server_version <= install.convert_version("1.2.5"):
                java_path = 6
            if install.convert_version("1.3") <= server_version <= install.convert_version("1.5.2"):
                java_path = 6
            elif install.convert_version("1.6") <= server_version <= install.convert_version("1.7.9"):
                java_path = 7
            elif install.convert_version("1.7.10") <= server_version <= install.convert_version("1.11.2"):
                java_path = 8
            elif install.convert_version("1.12") <= server_version <= install.convert_version("1.16.5"):
                java_path = 11
            elif install.convert_version("1.17") <= server_version <= install.convert_version("1.19.4"):
                java_path = 17
            elif install.convert_version("1.20") <= server_version:
                java_path = 21
            else:
                return "Error java_version"
    
            return java_path

        except Exception as e:
            return None
    


    def java_path(server_version):
        appdata = os.environ.get('LOCALAPPDATA')
        
        java = {
            21: r"Torch Manager\Java\jdk-21.0.2\bin\javaw.exe", # Java 21
            17: r"Torch Manager\Java\jdk-17.0.2\bin\javaw.exe", # Java 17
            16: r"Torch Manager\Java\jdk-16.0.2\bin\javaw.exe", # Java 16
            11: r"Torch Manager\Java\jdk-11.0.2\bin\javaw.exe", # Java 11
            8: r"Torch Manager\Java\openlogic-openjdk-8u422-b05-windows-x64\bin\javaw.exe"  # Java 8
        }

        java_num = install.java_version(server_version)
        pattern = os.path.join(appdata, java[java_num])

        return pattern