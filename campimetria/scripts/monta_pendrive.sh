#!/usr/bin/bash
#sudo su

MOUNT_POINT="/media/eyetec/EXAMES"
TARGET_LABEL="EXAMES"

# Procura pelo dispositivo baseado no rótulo
DEVICE="/dev/disk/by-label/$TARGET_LABEL"

# Verifica se o dispositivo existe
if [ -e "$DEVICE" ]; then
    echo "Dispositivo encontrado: $DEVICE"

    # Verifica se o dispositivo já está montado
    if mount | grep -q "$MOUNT_POINT"; then
        echo "O dispositivo já está montado em $MOUNT_POINT. Nada a fazer."
    else
        # Cria o ponto de montagem, se não existir
        [ ! -d "$MOUNT_POINT" ] && sudo mkdir -p "$MOUNT_POINT"

        # Monta o dispositivo
        sudo mount "$DEVICE" "$MOUNT_POINT"

        if [ $? -eq 0 ]; then
            echo "Dispositivo montado com sucesso em $MOUNT_POINT!"
        else
            echo "Erro ao montar o dispositivo."
        fi
    fi
else
    echo "Erro: Nenhum dispositivo com o rótulo '$TARGET_LABEL' encontrado."
fi
