# Traffic Analysis System

Este projeto captura imagens de veículos usando uma webcam, identifica automaticamente suas matrículas e registra matrícula, data e hora (minuto e segundo) em um arquivo CSV, evitando duplicações por um intervalo de debounce configurável.

## Estrutura de pastas

```
.
├── app/
│   ├── camera.py
│   ├── recognition.py
│   ├── storage.py
│   └── web.py
├── static/
│   ├── style.css
│   └── chart.js
├── templates/
│   └── index.html
├── tests/
│   └── test_recognition.py
├── requirements.txt
└── README.md
```

## Requisitos de sistema

- Python 3.7+
- OpenCV
- Tesseract OCR

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu_usuario/traffic-analysis-system.git
   cd traffic-analysis-system
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Execução

Para iniciar a aplicação:
```bash
python3 -m app.web
```
Acesse `http://localhost:5000` no navegador.

## Testes

Para executar os testes automatizados:
```bash
pytest
```

## Execução no Raspberry Pi

1. Atualize o sistema e instale dependências de sistema:
   ```bash
   sudo apt update
   sudo apt install python3-venv python3-dev libatlas-base-dev libtesseract-dev tesseract-ocr
   ```
2. (Opcional) Habilite a câmera Pi (caso use o módulo oficial):
   ```bash
   sudo raspi-config
   # Interface Options -> Camera -> Enable
   sudo reboot
   ```
3. Conecte a câmera USB ou Pi Camera ao Raspberry Pi.
4. Execute a aplicação:
   ```bash
   python3 -m app.web
   ```
5. No navegador de outro dispositivo, acesse:
   ```
   http://<IP_do_Raspberry_Pi>:5000
   ```