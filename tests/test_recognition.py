"""Testes automatizados para o módulo de reconhecimento de matrículas."""

import cv2
import numpy as np
import app.recognition as recognition

def test_recognition_synthetic(monkeypatch):
    # Simula engine OCR para retornar a placa esperada
    monkeypatch.setattr(recognition, 'pytesseract', type('P', (), {'image_to_string': lambda img, config=None: 'ABC1234'}))
    # Cria imagem sintética com texto de placa
    img = np.zeros((100, 300, 3), dtype=np.uint8)
    cv2.putText(img, 'ABC1234', (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)
    plates = recognition.recognize_plate(img)
    assert 'ABC1234' in plates