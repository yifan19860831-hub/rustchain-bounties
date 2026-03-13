#!/usr/bin/env python3
"""
IBM 7094 Punched Card I/O

Emulates IBM 711 card reader and IBM 716 line printer
- 80-column punched cards
- 6-bit BCD character encoding
- 800 cards/minute read speed
- 150 lines/minute print speed

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""


class PunchedCard:
    """
    IBM 80-column punched card simulation
    
    Standard card format used by IBM 7094:
    - 80 columns × 12 rows
    - 6-bit BCD character encoding
    - 6 characters per 36-bit word
    """
    
    def __init__(self):
        """Initialize punched card I/O"""
        self.columns = 80
        self.current_card = None
        self.cards_read = 0
        self.cards_punched = 0
        
        # Character encoding tables
        self.bcd_to_char = self._init_bcd_table()
        self.char_to_bcd = {v: k for k, v in self.bcd_to_char.items()}
    
    def _init_bcd_table(self):
        """Initialize 6-bit BCD encoding table"""
        table = {
            0b000000: ' ',   # Null/space
            0b000001: '1',
            0b000010: '2',
            0b000011: '3',
            0b000100: '4',
            0b000101: '5',
            0b000110: '6',
            0b000111: '7',
            0b001000: '8',
            0b001001: '9',
            0b001010: '0',
            0b001011: '&',
            0b001100: '-',
            0b001101: '+',
            0b001110: '*',
            0b001111: '/',
            0b010000: ' ',   # Space
            0b010001: '.',
            0b010010: ',',
            0b010011: "'",
            0b010100: '(',
            0b010101: ')',
            0b010110: '=',
            0b100001: 'A',
            0b100010: 'B',
            0b100011: 'C',
            0b100100: 'D',
            0b100101: 'E',
            0b100110: 'F',
            0b100111: 'G',
            0b101000: 'H',
            0b101001: 'I',
            0b101010: 'J',
            0b101011: 'K',
            0b101100: 'L',
            0b101101: 'M',
            0b101110: 'N',
            0b101111: 'O',
            0b110000: 'P',
            0b110001: 'Q',
            0b110010: 'R',
            0b110011: 'S',
            0b110100: 'T',
            0b110101: 'U',
            0b110110: 'V',
            0b110111: 'W',
            0b111000: 'X',
            0b111001: 'Y',
            0b111010: 'Z',
        }
        return table
    
    def encode_character(self, char):
        """
        Encode a character to 6-bit BCD
        
        Args:
            char: Character to encode
            
        Returns:
            6-bit BCD value
        """
        char = char.upper()
        if char in self.char_to_bcd:
            return self.char_to_bcd[char]
        return 0  # Default to space
    
    def decode_character(self, bcd_value):
        """
        Decode 6-bit BCD to character
        
        Args:
            bcd_value: 6-bit BCD value
            
        Returns:
            Character
        """
        return self.bcd_to_char.get(bcd_value & 0x3F, ' ')
    
    def encode_word(self, word):
        """
        Encode a 36-bit word to 6 characters
        
        Args:
            word: 36-bit integer
            
        Returns:
            String of 6 characters
        """
        chars = []
        for i in range(5, -1, -1):
            bcd = (word >> (i * 6)) & 0x3F
            chars.append(self.decode_character(bcd))
        return ''.join(chars)
    
    def decode_word(self, text):
        """
        Decode 6 characters to a 36-bit word
        
        Args:
            text: String of up to 6 characters
            
        Returns:
            36-bit integer
        """
        word = 0
        for i, char in enumerate(text[:6]):
            bcd = self.encode_character(char)
            word |= (bcd << ((5 - i) * 6))
        return word
    
    def read_card(self, card_data):
        """
        Simulate reading a punched card
        
        Args:
            card_data: String of 80 characters
            
        Returns:
            List of 36-bit words (14 words for 80 columns)
        """
        if len(card_data) != 80:
            raise ValueError("Card must be exactly 80 columns")
        
        self.cards_read += 1
        
        # Convert 80 characters to 36-bit words (6 chars/word)
        # 80 columns / 6 = 13.33, so we need 14 words
        words = []
        for i in range(0, 80, 6):
            chunk = card_data[i:i+6]
            word = self.decode_word(chunk.ljust(6))
            words.append(word)
        
        self.current_card = words
        return words
    
    def punch_card(self, words):
        """
        Simulate punching a card from words
        
        Args:
            words: List of 36-bit words
            
        Returns:
            String of 80 characters (punched card image)
        """
        self.cards_punched += 1
        
        # Convert words to 80-character card
        card = []
        for word in words[:14]:  # Max 14 words for 80 columns
            chars = self.encode_word(word)
            card.append(chars)
        
        card_text = ''.join(card)[:80].ljust(80)
        self.current_card = card_text
        return card_text
    
    def punch(self, text):
        """
        Punch a text string onto a card
        
        Args:
            text: Text to punch (up to 80 characters)
            
        Returns:
            Punched card string
        """
        card = text[:80].ljust(80)
        self.cards_punched += 1
        self.current_card = card
        return card
    
    def print_card(self, card_data=None):
        """
        Print a card image (simulates line printer)
        
        Args:
            card_data: Card data to print (uses current_card if None)
        """
        if card_data is None:
            card_data = self.current_card
        
        if card_data is None:
            print("(no card data)")
            return
        
        # Print card image
        if isinstance(card_data, list):
            # Word format
            text = ''.join([self.encode_word(w) for w in card_data])[:80]
        else:
            # String format
            text = str(card_data)[:80]
        
        print(f"|{text}|")
    
    def get_statistics(self):
        """Get I/O statistics"""
        return {
            'cards_read': self.cards_read,
            'cards_punched': self.cards_punched,
            'columns': self.columns,
            'current_card': self.current_card,
        }
    
    def dump(self):
        """Dump statistics and current card"""
        print("Punched Card I/O Statistics:")
        print("-" * 40)
        stats = self.get_statistics()
        print(f"  Cards read: {stats['cards_read']}")
        print(f"  Cards punched: {stats['cards_punched']}")
        print(f"  Columns: {stats['columns']}")
        
        if stats['current_card']:
            print()
            print("  Current card:")
            self.print_card()
        
        print()


def main():
    """Test punched card I/O"""
    print("IBM 7094 Punched Card Test")
    print("=" * 60)
    print()
    
    # Create card I/O
    card = PunchedCard()
    
    # Test character encoding
    print("Testing character encoding...")
    test_chars = 'A', 'Z', '0', '9', ' ', '.', ','
    for char in test_chars:
        bcd = card.encode_character(char)
        decoded = card.decode_character(bcd)
        status = "✓" if decoded == char.upper() else "✗"
        print(f"  {status} '{char}' -> BCD {bcd:06b} -> '{decoded}'")
    
    print()
    
    # Test word encoding
    print("Testing word encoding...")
    test_word = 0b100001100010100011100100101001001001  # "ABCDEF" in BCD
    encoded = card.encode_word(test_word)
    decoded = card.decode_word(encoded)
    print(f"  Original: {test_word:010o}")
    print(f"  Encoded:  '{encoded}'")
    print(f"  Decoded:  {decoded:010o}")
    
    print()
    
    # Test card punching
    print("Testing card punching...")
    card_text = "START    CLA      EPOCH     Load epoch counter"
    punched = card.punch(card_text)
    print(f"  Text:   '{card_text}'")
    print(f"  Punched ({len(punched)} columns):")
    card.print_card()
    
    print()
    
    # Test card reading
    print("Testing card reading...")
    read_card = "000100 CLA 000400 Load epoch"
    words = card.read_card(read_card.ljust(80))
    print(f"  Card:   '{read_card}'")
    print(f"  Words:  {len(words)} words")
    for i, word in enumerate(words[:5]):
        print(f"    Word {i}: {word:010o}")
    
    print()
    
    # Dump statistics
    card.dump()
    
    print("Punched card test complete!")


if __name__ == '__main__':
    main()
