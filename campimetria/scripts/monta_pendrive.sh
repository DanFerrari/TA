#!/usr/bin/env bash

MOUNT_POINT="/media/eyetec/EXAMES"
TARGET_LABEL="EXAMES"
DEVICE="/dev/disk/by-label/$TARGET_LABEL"

# Função para montar
montar_dispositivo() {
    echo "Dispositivo encontrado: $DEVICE"

    # Verifica se já está montado
    if mount | grep -q "$MOUNT_POINT"; then
        echo "O dispositivo já está montado em $MOUNT_POINT. Nada a fazer."
    else
        # Cria ponto de montagem se não existir
        [ ! -d "$MOUNT_POINT" ] && sudo mkdir -p "$MOUNT_POINT"

        # Monta o dispositivo
        sudo mount "$DEVICE" "$MOUNT_POINT"
        if [ $? -eq 0 ]; then
            echo "Dispositivo montado com sucesso em $MOUNT_POINT!"
        else
            echo "Erro ao montar o dispositivo."
            exit 1
        fi
    fi
}

# Função para esperar remoção e desmontar
aguardar_remocao() {
    echo "Aguardando remoção do dispositivo..."
    while [ -e "$DEVICE" ]; do
        sleep 2
    done

    echo "Dispositivo removido!"

    # Se ainda estiver montado, desmonta
    if mount | grep -q "$MOUNT_POINT"; then
        echo "Desmontando $MOUNT_POINT..."
        sudo umount "$MOUNT_POINT"
        echo "Dispositivo desmontado."
    fi
}

# Execução
if [ -e "$DEVICE" ]; then
    montar_dispositivo
    aguardar_remocao
else
    echo "Erro: Nenhum dispositivo com o rótulo '$TARGET_LABEL' encontrado."
fi
