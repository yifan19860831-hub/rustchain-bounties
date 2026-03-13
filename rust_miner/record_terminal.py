#!/usr/bin/env python3
"""
Terminal session recorder for Windows
Records command execution and outputs to asciinema .cast format
"""

import subprocess
import json
import time
import sys
import os
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

class TerminalRecorder:
    def __init__(self, output_file):
        self.output_file = output_file
        self.start_time = time.time()
        self.records = []
        self.width, self.height = 120, 40
        
    def get_timestamp(self):
        return time.time() - self.start_time
    
    def record_output(self, text, output_type='stdout'):
        """Record terminal output"""
        timestamp = self.get_timestamp()
        self.records.append([timestamp, 'o', text])
        print(text, end='')
    
    def record_input(self, text):
        """Record user input"""
        timestamp = self.get_timestamp()
        self.records.append([timestamp, 'i', text])
    
    def save(self):
        """Save recording to asciinema .cast format"""
        header = {
            'version': 2,
            'width': self.width,
            'height': self.height,
            'timestamp': int(self.start_time),
            'env': {
                'shell': 'powershell',
                'term': 'xterm'
            }
        }
        
        with open(self.output_file, 'w') as f:
            f.write(json.dumps(header) + '\n')
            for record in self.records:
                f.write(json.dumps(record) + '\n')
        
        print(f"\nRecording saved to: {self.output_file}")

def run_command(recorder, command, description):
    """Run a command and record its output"""
    recorder.record_output(f"\n\r\n❯ {description}\r\n")
    recorder.record_output(f"\r\n$ {command}\r\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.stdout:
            recorder.record_output(result.stdout)
        if result.stderr:
            recorder.record_output(result.stderr)
        if result.returncode == 0:
            recorder.record_output(f"\r\n✅ Command completed successfully\r\n")
        else:
            recorder.record_output(f"\r\n❌ Command failed with code {result.returncode}\r\n")
            
    except subprocess.TimeoutExpired:
        recorder.record_output("\r\n⏰ Command timed out\r\n")
    except Exception as e:
        recorder.record_output(f"\r\nError: {str(e)}\r\n")

def main():
    if len(sys.argv) < 2:
        output_file = "installation.cast"
    else:
        output_file = sys.argv[1]
    
    recorder = TerminalRecorder(output_file)
    
    print("🎬 RustChain Miner Installation Recorder")
    print("=" * 50)
    
    # Record installation steps
    commands = [
        ("rustc --version", "Checking Rust installation"),
        ("cargo --version", "Checking Cargo installation"),
        ("cargo build --release", "Building RustChain Miner (this may take a while)"),
        ("dir target\\release\\rustchain-miner.exe", "Verifying binary creation"),
        ("copy config.example.toml config.toml", "Creating configuration file"),
        ("type config.toml", "Showing configuration"),
    ]
    
    for cmd, desc in commands:
        run_command(recorder, cmd, desc)
        time.sleep(0.5)
    
    recorder.record_output("\n\r\n🎉 Installation complete!\r\n")
    recorder.record_output(f"\r\nBinary: target\\release\\rustchain-miner.exe\r\n")
    recorder.record_output(f"\r\nConfig: config.toml\r\n")
    
    recorder.save()
    
    # Also create a text version for easy viewing
    txt_file = output_file.replace('.cast', '.txt')
    with open(txt_file, 'w', encoding='utf-8') as f:
        for record in recorder.records:
            if record[1] == 'o':
                f.write(record[2])
    
    print(f"Text version saved to: {txt_file}")

if __name__ == '__main__':
    main()
