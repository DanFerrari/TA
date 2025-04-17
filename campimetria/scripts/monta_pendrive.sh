#!/usr/bin/env bash

MOUNT_LABEL="EXAMES"
DEVICE_PATH="/dev/disk/by-label/$MOUNT_LABEL"
DESIRED_MOUNT="/media/eyetec/$MOUNT_LABEL"

# Desmonta todos os pontos que contenham o label
for mnt in $(mount | grep "$MOUNT_LABEL" | awk '{print $3}'); do
    echo "Desmontando $mnt..."
    sudo umount -lf "$mnt"
done

# Remove diretório de montagem se existir
if [ -d "$DESIRED_MOUNT" ]; then
    echo "Removendo diretório de montagem antigo: $DESIRED_MOUNT"
    sudo rm -rf "$DESIRED_MOUNT"
fi

# Espera o sistema reconhecer o dispositivo
sleep 1

# Verifica se o dispositivo ainda está presente
if [ -e "$DEVICE_PATH" ]; then
    echo "Dispositivo encontrado: $DEVICE_PATH"
    
    sudo mkdir -p "$DESIRED_MOUNT"
    sudo mount "$DEVICE_PATH" "$DESIRED_MOUNT"

    if [ $? -eq 0 ]; then
        echo "Montado com sucesso em $DESIRED_MOUNT"
    else
        echo "Erro ao montar dispositivo."
        exit 1
    fi
else
    echo "Dispositivo '$MOUNT_LABEL' não encontrado."
    exit 1
fi
