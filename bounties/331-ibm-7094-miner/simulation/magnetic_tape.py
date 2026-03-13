#!/usr/bin/env python3
"""
IBM 7094 Magnetic Tape I/O

Emulates IBM 729 magnetic tape drives
- 7-track tape (6 data + 1 parity)
- 200, 556, or 800 characters per inch
- 112.5 inches per second
- Start/stop time: 7.5 ms

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""

import struct
from datetime import datetime


class MagneticTape:
    """
    IBM 729 Magnetic Tape Drive simulation
    
    Specifications:
    - 7 tracks (6 data + 1 parity)
    - Density: 200, 556, or 800 CPI
    - Speed: 112.5 inches/second
    - Start/stop time: 7.5 ms
    - Gap between records: 0.6 inches
    """
    
    def __init__(self, drive_number=0, density=800):
        """
        Initialize magnetic tape drive
        
        Args:
            drive_number: Drive number (0-9 per channel)
            density: Characters per inch (200, 556, or 800)
        """
        self.drive_number = drive_number
        self.density = density  # CPI
        self.speed = 112.5  # inches per second
        self.start_stop_time = 0.0075  # 7.5 ms
        
        # Tape state
        self.loaded = False
        self.tape_position = 0  # In inches
        self.records = []  # List of (position, data) tuples
        self.current_file = 0
        
        # Statistics
        self.reads = 0
        self.writes = 0
        self.rewinds = 0
    
    def initialize(self):
        """Initialize tape drive"""
        self.loaded = False
        self.tape_position = 0
        self.records = []
        self.current_file = 0
        self.reads = 0
        self.writes = 0
        self.rewinds = 0
    
    def load_tape(self, records=None):
        """
        Load a tape
        
        Args:
            records: Optional list of initial records
        """
        self.loaded = True
        self.tape_position = 0
        self.current_file = 0
        
        if records:
            self.records = records
        else:
            self.records = []
    
    def unload_tape(self):
        """Unload the tape"""
        self.loaded = False
        self.tape_position = 0
    
    def rewind(self):
        """Rewind tape to beginning"""
        if not self.loaded:
            return -1  # No tape
        
        self.tape_position = 0
        self.current_file = 0
        self.rewinds += 1
        
        # Simulate rewind time (depends on tape length)
        # Assume ~2400 feet tape, rewinds in ~3 minutes
        rewind_time = 180  # seconds (simulated)
        
        return 0  # Success
    
    def write_record(self, data):
        """
        Write a record to tape
        
        Args:
            data: Binary data to write
            
        Returns:
            Status code (0 = success)
        """
        if not self.loaded:
            return -1  # No tape loaded
        
        # Calculate record size in inches
        record_size = len(data) / self.density
        
        # Add gap (0.6 inches)
        total_size = record_size + 0.6
        
        # Store record
        self.records.append({
            'position': self.tape_position,
            'size': record_size,
            'data': data,
            'timestamp': datetime.now().isoformat(),
        })
        
        # Advance tape position
        self.tape_position += total_size
        self.writes += 1
        
        return 0  # Success
    
    def read_record(self):
        """
        Read a record from tape
        
        Returns:
            Binary data or None if end of tape
        """
        if not self.loaded:
            return None  # No tape loaded
        
        # Find record at current position
        for record in self.records:
            if abs(record['position'] - self.tape_position) < 0.1:
                # Found record
                self.tape_position += record['size'] + 0.6  # Skip record + gap
                self.reads += 1
                return record['data']
        
        # No record at current position (end of tape or gap)
        return None
    
    def skip_records(self, count):
        """
        Skip forward on tape
        
        Args:
            count: Number of records to skip
            
        Returns:
            Number of records actually skipped
        """
        if not self.loaded:
            return 0
        
        skipped = 0
        for i in range(count):
            record = self.read_record()
            if record is not None:
                skipped += 1
            else:
                break
        
        return skipped
    
    def write_file(self, records):
        """
        Write a file (multiple records) to tape
        
        Args:
            records: List of binary records
        """
        for record in records:
            self.write_record(record)
        
        # Write end-of-file marker (tape mark)
        self.write_record(b'\x00\x00\x00')  # Simplified tape mark
    
    def read_file(self):
        """
        Read a file from tape
        
        Returns:
            List of records, or None at end of tape
        """
        records = []
        
        while True:
            record = self.read_record()
            if record is None:
                break
            
            # Check for end-of-file marker
            if record == b'\x00\x00\x00':
                self.current_file += 1
                break
            
            records.append(record)
        
        return records if records else None
    
    def get_tape_length(self):
        """Get total tape length used (in inches)"""
        if not self.records:
            return 0.0
        last_record = self.records[-1]
        return last_record['position'] + last_record['size']
    
    def get_tape_length_feet(self):
        """Get total tape length used (in feet)"""
        return self.get_tape_length() / 12.0
    
    def get_statistics(self):
        """Get tape drive statistics"""
        return {
            'drive_number': self.drive_number,
            'density': self.density,
            'speed': self.speed,
            'loaded': self.loaded,
            'position_inches': self.tape_position,
            'position_feet': self.tape_position / 12.0,
            'records': len(self.records),
            'reads': self.reads,
            'writes': self.writes,
            'rewinds': self.rewinds,
            'files': self.current_file + 1,
        }
    
    def dump(self):
        """Dump tape status"""
        print(f"IBM 729 Tape Drive {self.drive_number}:")
        print("=" * 50)
        
        stats = self.get_statistics()
        print(f"  Density: {stats['density']} CPI")
        print(f"  Speed: {stats['speed']} inches/sec")
        print(f"  Loaded: {stats['loaded']}")
        print(f"  Position: {stats['position_feet']:.2f} feet")
        print(f"  Records: {stats['records']}")
        print(f"  Files: {stats['files']}")
        print(f"  Reads: {stats['reads']}")
        print(f"  Writes: {stats['writes']}")
        print(f"  Rewinds: {stats['rewinds']}")
        
        if self.records:
            print()
            print("  Record summary:")
            for i, record in enumerate(self.records[:10]):
                size = len(record['data'])
                print(f"    Record {i+1}: {size} bytes at {record['position']:.2f}\"")
            
            if len(self.records) > 10:
                print(f"    ... and {len(self.records) - 10} more records")
        
        print()


def main():
    """Test magnetic tape I/O"""
    print("IBM 729 Magnetic Tape Test")
    print("=" * 60)
    print()
    
    # Create tape drive
    tape = MagneticTape(drive_number=0, density=800)
    
    print(f"Drive: {tape.drive_number}")
    print(f"Density: {tape.density} CPI")
    print(f"Speed: {tape.speed} inches/sec")
    print()
    
    # Load tape
    print("Loading tape...")
    tape.load_tape()
    print(f"  Loaded: {tape.loaded}")
    print()
    
    # Write some records
    print("Writing records...")
    test_data = [
        b'EPOCH:000001',
        b'PROOF:12345678',
        b'WALLET:RTC4325',
        b'TIMESTAMP:2026-03-13',
    ]
    
    for data in test_data:
        status = tape.write_record(data)
        print(f"  Wrote {len(data)} bytes: status={status}")
    
    print()
    
    # Rewind and read
    print("Rewinding tape...")
    tape.rewind()
    print(f"  Position after rewind: {tape.tape_position:.2f}\"")
    print()
    
    print("Reading records...")
    tape.reads = 0  # Reset for demo
    while True:
        record = tape.read_record()
        if record is None:
            break
        print(f"  Read: {record}")
    
    print()
    
    # Dump statistics
    tape.dump()
    
    print("Magnetic tape test complete!")


if __name__ == '__main__':
    main()
