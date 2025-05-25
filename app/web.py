#!/usr/bin/env python3
"""Módulo web para servir interface usando Flask."""

from flask import Flask, render_template, request
from datetime import datetime, timedelta
from threading import Thread
from .camera import Camera
from .recognition import recognize_plate
from .storage import Storage

app = Flask(__name__)
storage = Storage()
camera = Camera().start()

def capture_loop():
    while True:
        frame = camera.read()
        if frame is not None:
            plates = recognize_plate(frame)
            for plate in plates:
                storage.add_plate(plate)

if __name__ == '__main__':
    thread = Thread(target=capture_loop, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000)

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
        {'plate': r['plate'], 'timestamp': r['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
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