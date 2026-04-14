#!/usr/bin/env python3
\"\"\"Structured JSON Logging for VPN Tests
Timestamped entries with levels.\"\"\"
import json
import sys
from datetime import datetime

class Logger:
    def __init__(self, log_file='vpn_demo.json'):
        self.log_file = log_file
        self.entries = self.load_logs()
    
    def load_logs(self):
        \"\"\"Load existing logs.\"\"\"
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def log(self, message, level='INFO'):
        \"\"\"Log entry with timestamp/level.\"\"\"
        entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        self.entries.append(entry)
        print(f'[{level}] {message}')
        self.save()
    
    def save(self):
        \"\"\"Save to JSON.\"\"\"
        with open(self.log_file, 'w') as f:
            json.dump(self.entries, f, indent=2)
    
    def summary(self):
        \"\"\"Print log summary.\"\"\"
        levels = {}
        for entry in self.entries[-20:]:  # Last 20
            level = entry['level']
            levels[level] = levels.get(level, 0) + 1
        
        print('\\n=== LOG SUMMARY ===')
        for level, count in levels.items():
            print(f'{level}: {count}')
        print('===================')

if __name__ == '__main__':
    log = Logger()
    log.log('Logger test')
    log.summary()

