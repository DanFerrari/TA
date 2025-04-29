#!/bin/bash

# Atualizar pacotes
sudo apt update

# Baixar o instalador do TeamViewer
echo "Baixando TeamViewer..."
wget https://download.teamviewer.com/download/linux/teamviewer_arm64.deb -O /tmp/teamviewer_arm64.deb

# Instalar o pacote
echo "Instalando TeamViewer..."
sudo dpkg --configure -a
sudo apt install -y /tmp/teamviewer_arm64.deb

# Resolver dependências quebradas (caso existam)
sudo apt --fix-broken install -y

# Abrir o TeamViewer
echo "Abrindo TeamViewer..."
teamviewer
