#!/bin/bash

# Atualizar pacotes
sudo apt update

# Instalar o TeamViewer a partir do pendrive
echo "Instalando TeamViewer..."
sudo apt install -y "$(dirname "$0")/teamviewer_arm64.deb"

# Resolver dependências quebradas (caso existam)
sudo apt --fix-broken install -y

# Abrir o TeamViewer
echo "Abrindo TeamViewer..."
teamviewer &
