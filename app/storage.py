#!/usr/bin/env python3
"""Módulo para armazenamento dos dados de matrículas em CSV com debounce."""

import csv
from datetime import datetime
import threading
import os
import cv2

class Storage:
    def __init__(self, csv_file='plates.csv', debounce_seconds=60):
        self.csv_file = csv_file
        self.debounce_seconds = debounce_seconds
        self.lock = threading.Lock()
        self.last_seen = {}

        basedir = os.path.abspath(os.path.dirname(__file__))
        self.images_dir = os.path.abspath(
            os.path.join(basedir, os.pardir, 'static', 'captures')
        )
        os.makedirs(self.images_dir, exist_ok=True)

        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['plate', 'timestamp', 'image'])

    def add_plate(self, plate, image=None):
        now = datetime.now()
        with self.lock:
            last = self.last_seen.get(plate)
            if last and (now - last).total_seconds() < self.debounce_seconds:
                return False
            image_filename = ''
            if image is not None:
                image_filename = f"{plate}_{now.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
                image_path = os.path.join(self.images_dir, image_filename)
                cv2.imwrite(image_path, image)
            with open(self.csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([plate, now.isoformat(), image_filename])
            self.last_seen[plate] = now
            return True

    def get_records(self):
        records = []
        with self.lock:
            with open(self.csv_file, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ts = datetime.fromisoformat(row['timestamp'])
                    records.append({
                        'plate': row['plate'],
                        'timestamp': ts,
                        'image': row.get('image')
                    })
        return records