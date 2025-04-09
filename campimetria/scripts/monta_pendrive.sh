#!/usr/bin/env bash

MOUNT_POINT="/media/eyetec/EXAMES"
TARGET_LABEL="EXAMES"
DEVICE="/dev/disk/by-label/$TARGET_LABEL"

# Verifica se o dispositivo existe
if [ -e "$DEVICE" ]; then
    echo "Dispositivo encontrado: $DEVICE"

    # Cria o ponto de montagem, se não existir
    [ ! -d "$MOUNT_POINT" ] && sudo mkdir -p "$MOUNT_POINT"

    # Verifica se já está montado
    if mount | grep -q "$MOUNT_POINT"; then
        echo "Dispositivo já está montado. Desmontando..."
        sudo umount "$MOUNT_POINT"
    fi

    # Monta o dispositivo
    sudo mount "$DEVICE" "$MOUNT_POINT"
    if [ $? -eq 0 ]; then
        echo "Dispositivo montado com sucesso em $MOUNT_POINT!"
    else
        echo "Erro ao montar o dispositivo."
        exit 1
    fi
else
    echo "Erro: Nenhum dispositivo com o rótulo '$TARGET_LABEL' encontrado."
    exit 1
fi
