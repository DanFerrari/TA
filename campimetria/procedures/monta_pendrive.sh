#!/bin/bash

MOUNT_POINT="/media/eyetec"
TARGET_LABEL="EXAMES"

# Obtém o nome do dispositivo (e.g., /dev/sdb1)
DEVICE=$1

# Obtém o rótulo (label) do sistema de arquivos
DEVICE_LABEL=$(blkid -o value -s LABEL "$DEVICE")

# Verifica se o rótulo corresponde ao desejado
if [ "$DEVICE_LABEL" == "$TARGET_LABEL" ]; then
    # Cria o ponto de montagem, se não existir
    [ ! -d "$MOUNT_POINT" ] && mkdir -p "$MOUNT_POINT"

    # Monta o dispositivo
    mount "$DEVICE" "$MOUNT_POINT"
    echo "Dispositivo montado em $MOUNT_POINT"
else
    echo "O dispositivo não possui o rótulo esperado."
fi
