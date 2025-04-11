#!/usr/bin/env bash

MOUNT_LABEL="EXAMES"
DEVICE_PATH="/dev/disk/by-label/$MOUNT_LABEL"
DESIRED_MOUNT="/media/eyetec/$MOUNT_LABEL"

# Verifica se já existe algo montado no ponto de montagem desejado
if mountpoint -q "$DESIRED_MOUNT"; then
    echo "Já existe algo montado em $DESIRED_MOUNT. Desmontando..."
    sudo umount "$DESIRED_MOUNT"
    sudo rm -rf "$DESIRED_MOUNT"
    if [ $? -eq 0 ]; then
        echo "Desmontado com sucesso."
    else
        echo "Erro ao desmontar $DESIRED_MOUNT."
        exit 1
    fi
fi

# Função para descobrir onde está montado
get_actual_mount_point() {
    grep "$DEVICE_PATH" /proc/mounts | awk '{print $2}'
}

# Verifica se o dispositivo existe
if [ -e "$DEVICE_PATH" ]; then
    echo "Dispositivo encontrado: $DEVICE_PATH"

    # Verifica onde está montado, se estiver
    CURRENT_MOUNT=$(get_actual_mount_point)

    # Se estiver montado em outro lugar, desmonta
    if [ -n "$CURRENT_MOUNT" ] && [ "$CURRENT_MOUNT" != "$DESIRED_MOUNT" ]; then
        echo "Dispositivo montado em '$CURRENT_MOUNT'. Desmontando para montar em '$DESIRED_MOUNT'."
        sudo umount "$CURRENT_MOUNT"
    fi

    # Cria o ponto de montagem se não existir
    [ ! -d "$DESIRED_MOUNT" ] && sudo mkdir -p "$DESIRED_MOUNT"

    # Se já estiver montado no local desejado
    if mount | grep -q "$DESIRED_MOUNT"; then
        echo "Dispositivo já montado em $DESIRED_MOUNT"
    else
        # Monta no local desejado
        sudo mount "$DEVICE_PATH" "$DESIRED_MOUNT"
        if [ $? -eq 0 ]; then
            echo "Dispositivo montado com sucesso em $DESIRED_MOUNT"
        else
            echo "Erro ao montar o dispositivo."
            exit 1
        fi
    fi
else
    echo "Dispositivo '$MOUNT_LABEL' não encontrado."

    # Caso o ponto de montagem ainda exista, mas o dispositivo foi removido
    if mountpoint -q "$DESIRED_MOUNT"; then
        echo "Desmontando ponto de montagem órfão..."
        sudo umount "$DESIRED_MOUNT"
    fi

    exit 1
fi
