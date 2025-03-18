#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys
import shutil

import OPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.SUNXI)   

PIN_ENTRADA = 'PD22'
PIN_SAIDA = 'PL08'

GPIO.setup(PIN_ENTRADA, GPIO.IN)

GPIO.setup(PIN_SAIDA, GPIO.OUT)
GPIO.output(PIN_SAIDA,GPIO.HIGH)


try:
        while True:
            estado = GPIO.input(PIN_ENTRADA)  # Lê o pino
          
            if estado == GPIO.HIGH:
                print("Botão pressionado!")
                GPIO.output(PIN_SAIDA,GPIO.HIGH)
                 # Pequeno delay para evitar leituras muito rápidas
            else:
                print("Botão solto!")
                print(GPIO.input(PIN_ENTRADA))
                GPIO.output(PIN_SAIDA,GPIO.LOW)
                  # Pequeno delay para evitar leituras muito rápidas
except KeyboardInterrupt:
    print("\nEncerrando...")
    GPIO.cleanup()  # Libera os pinos ao sair