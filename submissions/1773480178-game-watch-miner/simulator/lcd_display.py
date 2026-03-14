"""
Segmented LCD Display Emulation

Emulates the segmented LCD display of the original Game & Watch.
The display consists of fixed segments that can be turned on/off.
"""

from dataclasses import dataclass, field
from typing import Set, Dict, List
from enum import Enum
from datetime import datetime


class LCDSegment(Enum):
    """Defines all segments available on the Game & Watch LCD"""
    
    # Time display segments (4 digits for HH:MM)
    TIME_H1_A = 0   # Hour tens, segment A
    TIME_H1_B = 1   # Hour tens, segment B
    TIME_H1_C = 2
    TIME_H1_D = 3
    TIME_H1_E = 4
    TIME_H1_F = 5
    TIME_H1_G = 6
    
    TIME_H2_A = 7   # Hour units
    TIME_H2_B = 8
    TIME_H2_C = 9
    TIME_H2_D = 10
    TIME_H2_E = 11
    TIME_H2_F = 12
    TIME_H2_G = 13
    
    TIME_M1_A = 14  # Minute tens
    TIME_M1_B = 15
    TIME_M1_C = 16
    TIME_M1_D = 17
    TIME_M1_E = 18
    TIME_M1_F = 19
    TIME_M1_G = 20
    
    TIME_M2_A = 21  # Minute units
    TIME_M2_B = 22
    TIME_M2_C = 23
    TIME_M2_D = 24
    TIME_M2_E = 25
    TIME_M2_F = 26
    TIME_M2_G = 27
    
    # Score/RTC display (3 digits)
    SCORE_1 = 28
    SCORE_2 = 29
    SCORE_3 = 30
    
    # Icon segments
    ICON_MINING = 31    # Pickaxe/mining icon
    ICON_BATTERY = 32   # Battery indicator
    ICON_CLOCK = 33     # Clock icon
    ICON_SIGNAL = 34    # Network signal
    
    # Labels
    LABEL_TIME = 35
    LABEL_SCORE = 36
    LABEL_RTC = 37


@dataclass
class SegmentedDisplay:
    """
    Emulates the segmented LCD display.
    
    The original Game & Watch used custom segmented LCDs where each
    "digit" or "icon" was a fixed pattern of segments etched into
    the display. Segments could be turned on/off by applying voltage.
    """
    
    # 7-segment patterns for digits 0-9
    # Segments: A, B, C, D, E, F, G (standard 7-segment layout)
    #    A
    #  F   B
    #    G
    #  E   C
    #    D
    SEGMENT_PATTERNS: Dict[int, List[bool]] = field(default_factory=lambda: {
        0: [1, 1, 1, 1, 1, 1, 0],  # 0
        1: [0, 1, 1, 0, 0, 0, 0],  # 1
        2: [1, 1, 0, 1, 1, 0, 1],  # 2
        3: [1, 1, 1, 1, 0, 0, 1],  # 3
        4: [0, 1, 1, 0, 0, 1, 1],  # 4
        5: [1, 0, 1, 1, 0, 1, 1],  # 5
        6: [1, 0, 1, 1, 1, 1, 1],  # 6
        7: [1, 1, 1, 0, 0, 0, 0],  # 7
        8: [1, 1, 1, 1, 1, 1, 1],  # 8
        9: [1, 1, 1, 1, 0, 1, 1],  # 9
    })
    
    # Currently active segments
    active_segments: Set[LCDSegment] = field(default_factory=set)
    
    def set_digit(self, position: int, value: int):
        """
        Set a digit at the given position (0-9).
        Position mapping depends on which display region.
        """
        if value < 0 or value > 9:
            return
        
        pattern = self.SEGMENT_PATTERNS[value]
        base_segment = position * 7
        
        # Map pattern to actual segments (simplified)
        for i, active in enumerate(pattern):
            if active:
                seg_num = base_segment + i
                if seg_num < 28:  # Only time digits
                    self.active_segments.add(LCDSegment(seg_num))
    
    def set_icon(self, icon: LCDSegment, active: bool = True):
        """Turn an icon segment on or off"""
        if active:
            self.active_segments.add(icon)
        else:
            self.active_segments.discard(icon)
    
    def clear(self):
        """Clear all segments"""
        self.active_segments.clear()
    
    def render_ascii(self) -> str:
        """
        Render the display as ASCII art for terminal display.
        This is a simplified representation.
        """
        lines = []
        
        # Top border
        lines.append("┌─────────────────────────────────┐")
        
        # Time display
        now = datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"
        lines.append(f"│  ⏰ TIME: {time_str:<20} │")
        
        # Mining icon status
        mining_active = LCDSegment.ICON_MINING in self.active_segments
        mining_str = "⛏️ MINING" if mining_active else "⏸ PAUSED"
        lines.append(f"│  STATUS: {mining_str:<21} │")
        
        # Spacer
        lines.append("│                                   │")
        
        # Badge display area (simulated segments)
        lines.append("│  ╔═══════════════════════════════╗│")
        lines.append("│  ║   RUSTCHAIN MINING BADGE      ║│")
        lines.append("│  ║                               ║│")
        
        # Simulated segment visualization
        segment_row = ""
        for i in range(27):
            if LCDSegment(i) in self.active_segments:
                segment_row += "█"
            else:
                segment_row += "░"
        
        lines.append(f"│  ║  {segment_row} ║│")
        lines.append("│  ║                               ║│")
        lines.append("│  ╚═══════════════════════════════╝│")
        
        # Bottom info
        lines.append("│                                   │")
        lines.append("│  🔋 BATTERY  │  📶 SIGNAL       │")
        lines.append("│                                   │")
        lines.append("│  🎮 GAME & WATCH • Nintendo 1980 │")
        
        # Bottom border
        lines.append("└─────────────────────────────────┘")
        
        return "\n".join(lines)
    
    def render_minimal(self) -> str:
        """Render a minimal single-line display"""
        now = datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"
        mining = "⛏️" if LCDSegment.ICON_MINING in self.active_segments else "⏸"
        return f"[{time_str}] {mining} Game&Watch Miner"
    
    def get_segment_count(self) -> int:
        """Return number of active segments"""
        return len(self.active_segments)
    
    def get_memory_bytes(self) -> int:
        """
        Calculate memory needed to store display state.
        Each segment = 1 bit, packed into bytes.
        """
        num_segments = len(LCDSegment)
        return (num_segments + 7) // 8  # Round up to nearest byte
