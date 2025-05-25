#!/usr/bin/env python3
"""Módulo para reconhecimento de matrículas usando OpenCV e Tesseract OCR."""

import cv2
try:
    import pytesseract
except ImportError:
    pytesseract = None
import re

def recognize_plate(image):
    """
    Reconhece placas em uma imagem e retorna lista de strings de matrículas.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    plates = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        ratio = w / float(h) if h > 0 else 0
        if 2 < ratio < 6 and w * h > 1000:
            plate_img = gray[y:y+h, x:x+w]
            text = pytesseract.image_to_string(
                plate_img,
                config='--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            )
            text = re.sub(r'[^A-Z0-9]', '', text)
            if 4 <= len(text) <= 10:
                plates.append(text)

    # Fallback: OCR de toda a imagem se não encontrar região de placa
    if plates or not pytesseract:
        return list(set(plates))
    text = pytesseract.image_to_string(
        gray,
        config='--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    )
    text = re.sub(r'[^A-Z0-9]', '', text)
    if 4 <= len(text) <= 10:
        plates.append(text)

    return list(set(plates))