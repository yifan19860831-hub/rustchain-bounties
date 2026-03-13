#!/usr/bin/env python3
"""
IBM 7094 Data Channel I/O

Emulates the 8 data channels of the IBM 7094
- Forerunner of modern DMA (Direct Memory Access)
- Each channel can control multiple devices
- Channels operate independently while CPU computes

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""


class DataChannel:
    """
    Single data channel for IBM 7094
    
    Each channel can control up to 10 devices (tape drives, etc.)
    Channels operate independently from the CPU
    """
    
    def __init__(self, channel_number):
        """
        Initialize data channel
        
        Args:
            channel_number: Channel ID (0-7)
        """
        self.channel_number = channel_number
        self.devices = []  # List of connected devices
        self.status = 0  # Channel status word
        self.busy = False
        self.current_command = None
        self.transfer_count = 0
        self.error_count = 0
    
    def connect_device(self, device):
        """Connect a device to this channel"""
        self.devices.append(device)
    
    def execute_command(self, command, device_address, memory_address, count):
        """
        Execute an I/O command
        
        Args:
            command: Command code (READ=01, WRITE=02, REWIND=03, etc.)
            device_address: Device address on channel
            memory_address: Memory address for transfer
            count: Number of words to transfer
            
        Returns:
            Status code
        """
        if self.busy:
            return -1  # Channel busy
        
        self.busy = True
        self.current_command = command
        self.transfer_count = count
        
        # Find device
        device = None
        for dev in self.devices:
            if dev.address == device_address:
                device = dev
                break
        
        if device is None:
            self.busy = False
            self.error_count += 1
            return -2  # Device not found
        
        # Execute command
        status = 0
        if command == 0x01:  # READ
            status = device.read(memory_address, count)
        elif command == 0x02:  # WRITE
            status = device.write(memory_address, count)
        elif command == 0x03:  # REWIND
            status = device.rewind()
        elif command == 0x04:  # SKIP
            status = device.skip(count)
        elif command == 0x05:  # SENSE
            status = device.sense()
        else:
            status = -3  # Invalid command
        
        self.busy = False
        self.current_command = None
        return status
    
    def get_status(self):
        """Get channel status"""
        return {
            'channel': self.channel_number,
            'busy': self.busy,
            'status': self.status,
            'devices': len(self.devices),
            'transfer_count': self.transfer_count,
            'error_count': self.error_count,
        }


class DataChannels:
    """
    Data channel controller for IBM 7094
    
    Manages 8 independent data channels for I/O operations
    """
    
    def __init__(self, channels=8):
        """
        Initialize data channel controller
        
        Args:
            channels: Number of channels (default 8 for IBM 7094)
        """
        self.channels = channels
        self.channel_list = [DataChannel(i) for i in range(channels)]
        self.command_table = {
            0x01: 'READ',
            0x02: 'WRITE',
            0x03: 'REWIND',
            0x04: 'SKIP',
            0x05: 'SENSE',
        }
    
    def initialize(self):
        """Initialize all channels"""
        for channel in self.channel_list:
            channel.busy = False
            channel.status = 0
            channel.transfer_count = 0
            channel.error_count = 0
    
    def get_channel(self, channel_number):
        """
        Get a specific channel
        
        Args:
            channel_number: Channel ID (0-7)
            
        Returns:
            DataChannel object
        """
        if channel_number < 0 or channel_number >= self.channels:
            raise ValueError(f"Channel {channel_number} out of range (0-{self.channels-1})")
        return self.channel_list[channel_number]
    
    def execute_io(self, channel_number, command, device_address, memory_address, count):
        """
        Execute an I/O operation on a channel
        
        Args:
            channel_number: Channel ID
            command: Command code
            device_address: Device address
            memory_address: Memory address
            count: Transfer count
            
        Returns:
            Status code
        """
        channel = self.get_channel(channel_number)
        return channel.execute_command(command, device_address, memory_address, count)
    
    def dump_status(self):
        """Dump status of all channels"""
        print("IBM 7094 Data Channel Status:")
        print("=" * 60)
        
        for channel in self.channel_list:
            status = channel.get_status()
            busy_str = "BUSY" if status['busy'] else "IDLE"
            print(f"  Channel {status['channel']}: {busy_str}")
            print(f"    Devices: {status['devices']}")
            print(f"    Errors: {status['error_count']}")
            print(f"    Transfers: {status['transfer_count']}")
            print()
        
        print("=" * 60)
        print(f"  Total channels: {self.channels}")
        print()


class TapeDrive:
    """
    IBM 729 Magnetic Tape Drive simulation
    
    Connected to data channels for I/O
    """
    
    def __init__(self, drive_number, channel=0):
        """
        Initialize tape drive
        
        Args:
            drive_number: Drive number (0-9 per channel)
            channel: Channel number this drive is connected to
        """
        self.drive_number = drive_number
        self.address = drive_number  # Device address = drive number
        self.channel = channel
        self.tape_position = 0
        self.records = []  # List of tape records
        self.loaded = False
    
    def load_tape(self, records):
        """Load a tape with records"""
        self.records = records
        self.tape_position = 0
        self.loaded = True
    
    def read(self, memory_address, count):
        """Read from tape to memory"""
        if not self.loaded:
            return -1  # No tape loaded
        
        if self.tape_position >= len(self.records):
            return -2  # End of tape
        
        # In real implementation, this would write to memory
        # For simulation, we just advance position
        self.tape_position += 1
        return 0  # Success
    
    def write(self, memory_address, count):
        """Write from memory to tape"""
        if not self.loaded:
            return -1  # No tape loaded
        
        # In real implementation, this would read from memory
        # For simulation, we just add a record
        self.records.append(0)
        self.tape_position += 1
        return 0  # Success
    
    def rewind(self):
        """Rewind tape"""
        self.tape_position = 0
        return 0  # Success
    
    def skip(self, count):
        """Skip forward on tape"""
        self.tape_position += count
        if self.tape_position > len(self.records):
            self.tape_position = len(self.records)
        return 0  # Success
    
    def sense(self):
        """Get drive status"""
        return {
            'drive': self.drive_number,
            'channel': self.channel,
            'loaded': self.loaded,
            'position': self.tape_position,
            'records': len(self.records),
        }


def main():
    """Test data channel emulation"""
    print("IBM 7094 Data Channel Test")
    print("=" * 60)
    print()
    
    # Create 8 data channels
    dc = DataChannels(channels=8)
    
    print(f"Number of channels: {dc.channels}")
    print()
    
    # Initialize channels
    dc.initialize()
    print("Channels initialized")
    print()
    
    # Connect tape drives to channel 0
    channel0 = dc.get_channel(0)
    for i in range(3):
        drive = TapeDrive(drive_number=i, channel=0)
        channel0.connect_device(drive)
        print(f"  Connected tape drive {i} to channel 0")
    
    print()
    
    # Test tape operations
    print("Testing tape operations...")
    drive = channel0.devices[0]
    drive.load_tape([1, 2, 3, 4, 5])
    print(f"  Tape loaded with {len(drive.records)} records")
    
    status = drive.read(0, 1)
    print(f"  Read status: {status}")
    print(f"  Tape position: {drive.tape_position}")
    
    drive.rewind()
    print(f"  After rewind: position = {drive.tape_position}")
    
    print()
    
    # Dump channel status
    dc.dump_status()
    
    print("Data channel test complete!")


if __name__ == '__main__':
    main()
