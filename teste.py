import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QEventLoop, QTimer, QObject, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

class EventFilter:
    """Filtro de eventos para capturar teclas pressionadas."""
    def __init__(self, tecla_pressionada, loop):
        self.tecla_pressionada = tecla_pressionada
        self.loop = loop

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            self.tecla_pressionada["valor"] = event.text()
            self.loop.quit()
            return True  # Indica que o evento foi tratado
        return False  # Continua processando outros eventos normalmente


def esperar_tecla_ou_timer(tempo_maximo=3000):
    """Pausa a execução e espera uma tecla ser pressionada ou o tempo limite estourar."""
    
    app = QApplication.instance()  # Usa a aplicação já existente
    if not app:
        raise RuntimeError("O QApplication precisa estar rodando!")

    loop = QEventLoop()  # Cria um loop de eventos para bloquear a execução
    tecla_pressionada = {"valor": None}  # Dicionário mutável para armazenar a tecla pressionada

    # Configura um timer para encerrar o loop após o tempo limite
    def timeout():
        if tecla_pressionada["valor"] is None:  # Só registra timeout se nenhuma tecla foi pressionada antes
            tecla_pressionada["valor"] = "timeout"
        loop.quit()  # Sai do loop e desbloqueia a execução

    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(timeout)
    timer.start(tempo_maximo)

    # Cria e instala o filtro de eventos
    event_filter = EventFilter()
    app.installEventFilter(event_filter)

    loop.exec_()  # Bloqueia a execução aqui até que uma tecla seja pressionada ou o tempo acabe

    app.removeEventFilter(event_filter)  # Remove o filtro de eventos depois do uso

    return tecla_pressionada["valor"]  # Retorna a tecla pressionada ou 'timeout'

# === Fluxo do Programa ===
app = QApplication(sys.argv)  # Cria uma instância de QApplication

print("Linha 1: Código antes da espera")

# Espera até o usuário pressionar uma tecla ou o tempo acabar
print("Aguardando interação...")
resposta = esperar_tecla_ou_timer(5000)  # Tempo máximo de 5 segundos

if resposta == "timeout":
    print("Tempo máximo atingido antes de qualquer tecla ser pressionada.")
else:
    print(f"Tecla '{resposta}' foi pressionada antes do tempo acabar!")
    class MainWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            self.label = QLabel("Pressione a tecla ESPAÇO para continuar...", self)
            self.label.setAlignment(Qt.AlignCenter)

            layout = QVBoxLayout()
            layout.addWidget(self.label)
            self.setLayout(layout)

            self.setWindowTitle('Esperar Tecla ou Timer')
            self.setGeometry(300, 300, 400, 200)

    # Cria a janela principal
    main_window = MainWindow()
    main_window.show()

    # Continua o fluxo do programa
    print("Linha 2: Código depois da espera")
    sys.exit(app.exec_())
# Continua o fluxo do programa
print("Linha 2: Código depois da espera")
