#!/bin/bash

#Check-OS
OS=$(uname -s)
ARCH=$(uname -m)
#example ./install jar_file.tar.gz sraprogram.zip
if [[ "$OS" == "Linux" ]];then
        if [ -e "$1" ]; then
                echo "OK"
                echo "Creating directory..."
                filenameJava=$(basename $1)
                nameJava="${filename%.*}"
                sudo tar -xvzf "$1" -C /opt/
                echo "export JAVA_HOME=/opt/$nameJava">> ~/.bashrc
                echo 'export PATH=$JAVA_HOME/bin:$PATH'>> ~/.bashrc
                source ~/.bashrc
                mkdir "$HOME/.SRAnal710"
                unzip "$2" -d "$HOME/.SRAnal710"
                touch SRAnal710.desktop
                echo "[Desktop Entry]" >> SRAnal710.desktop
                echo "Name=SRAnal710" >> SRAnal710.desktop
                echo "Comment=Run program SRAnal710" >> SRAnal710.desktop
                echo "/opt/jre1.8.0_461/bin/java -jar '$HOME/.SRAnal710/dist/SRAnal710e.jar'" >> SRAnal710.desktop
                echo "Terminal=false" >> SRAnal710.desktop
                echo "Type=Application" >> SRAnal710.desktop
                echo "Categories=Utility;" >> SRAnal710.desktop

                # Move the icon to the correct location
                mv SRAnal710.desktop ~/.local/share/applications/

        else
                echo "Doest not exist :$1"
        fi
else
        echo "Li"
fi
