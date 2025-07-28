"""
Simple logger utility for developer visibility.
"""
import datetime

def log(message: str):
    print(f"[{datetime.datetime.now().isoformat()}] {message}")
