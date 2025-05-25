#!/usr/bin/env python3
"""Módulo para armazenamento dos dados de matrículas em CSV com debounce."""

import csv
from datetime import datetime
import threading
import os

class Storage:
    def __init__(self, csv_file='plates.csv', debounce_seconds=60):
        self.csv_file = csv_file
        self.debounce_seconds = debounce_seconds
        self.lock = threading.Lock()
        self.last_seen = {}

        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['plate', 'timestamp'])

    def add_plate(self, plate):
        now = datetime.now()
        with self.lock:
            last = self.last_seen.get(plate)
            if last and (now - last).total_seconds() < self.debounce_seconds:
                return False
            with open(self.csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([plate, now.isoformat()])
            self.last_seen[plate] = now
            return True

    def get_records(self):
        records = []
        with self.lock:
            with open(self.csv_file, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ts = datetime.fromisoformat(row['timestamp'])
                    records.append({'plate': row['plate'], 'timestamp': ts})
        return records