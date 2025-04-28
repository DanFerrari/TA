#!/bin/bash

# Nome da interface de rede
INTERFACE="eth0"

# Parar serviço de rede se necessário
sudo ip addr flush dev $INTERFACE

# Solicitar IP via DHCP
sudo dhclient $INTERFACE

echo "Configuração de DHCP aplicada para $INTERFACE"
