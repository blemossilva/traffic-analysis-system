#!/usr/bin/env python3
"""Módulo web para servir interface usando Flask."""

import os
import cv2
from flask import Flask, render_template, request, Response
from datetime import datetime, timedelta
from threading import Thread
from .camera import Camera
from .recognition import recognize_plate
from .storage import Storage

basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.abspath(os.path.join(basedir, os.pardir, 'templates'))
static_dir = os.path.abspath(os.path.join(basedir, os.pardir, 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
storage = Storage()
camera = Camera().start()

def gen_frames():
    while True:
        frame = camera.read()
        if frame is None:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            ratio = w / float(h) if h > 0 else 0
            if 2 < ratio < 6 and w * h > 1000:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def capture_loop():
    while True:
        frame = camera.read()
        if frame is not None:
            plates = recognize_plate(frame)
            for plate in plates:
                storage.add_plate(plate, frame)


@app.route('/', methods=['GET'])
def index():
    try:
        hours = int(request.args.get('hours', 1))
    except ValueError:
        hours = 1
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    records = [r for r in storage.get_records() if start_time <= r['timestamp'] <= end_time]
    # Prepare table data
    table_records = [
        {
            'plate': r['plate'],
            'timestamp': r['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            'image': r.get('image')
        }
        for r in sorted(records, key=lambda x: x['timestamp'], reverse=True)
    ]
    # Prepare chart data
    counts = []
    labels = []
    for i in range(hours, 0, -1):
        segment_start = end_time - timedelta(hours=i)
        segment_end = end_time - timedelta(hours=i-1)
        count = sum(1 for r in records if segment_start <= r['timestamp'] < segment_end)
        labels.append(segment_start.strftime('%H:%M'))
        counts.append(count)
    return render_template('index.html', records=table_records, labels=labels, counts=counts, selected_hours=hours)

if __name__ == '__main__':
    thread = Thread(target=capture_loop, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000)