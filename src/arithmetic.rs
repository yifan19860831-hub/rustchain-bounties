//! 32-bit Arithmetic Library for PDP-8
//! Emulates 32-bit operations using three 12-bit words

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Word32 {
    pub low: u16,
    pub mid: u16,
    pub high: u16,
}

impl Word32 {
    pub const fn from_u32(value: u32) -> Self {
        Word32 {
            low: ((value & 0xFFF) as u16),
            mid: (((value >> 12) & 0xFFF) as u16),
            high: (((value >> 24) & 0xFF) as u16),
        }
    }

    pub fn to_u32(&self) -> u32 {
        ((self.high as u32) << 24) | ((self.mid as u32) << 12) | (self.low as u32)
    }

    pub fn add(self, other: Word32) -> (Word32, bool) {
        let sum_low = (self.low as u32) + (other.low as u32);
        let new_low = (sum_low & 0xFFF) as u16;
        let c1 = (sum_low >> 12) & 1;
        
        let sum_mid = (self.mid as u32) + (other.mid as u32) + c1;
        let new_mid = (sum_mid & 0xFFF) as u16;
        let c2 = (sum_mid >> 12) & 1;
        
        let sum_high = (self.high as u32) + (other.high as u32) + c2;
        let new_high = (sum_high & 0xFF) as u16;
        let carry = (sum_high >> 8) != 0;
        
        (Word32 { low: new_low, mid: new_mid, high: new_high }, carry)
    }

    pub fn add_wrapped(self, other: Word32) -> Word32 {
        let (result, _) = self.add(other);
        result
    }

    pub fn and(self, other: Word32) -> Word32 {
        Word32 { low: self.low & other.low, mid: self.mid & other.mid, high: self.high & other.high }
    }

    pub fn xor(self, other: Word32) -> Word32 {
        Word32 { low: self.low ^ other.low, mid: self.mid ^ other.mid, high: self.high ^ other.high }
    }

    pub fn not(self) -> Word32 {
        Word32 { low: (!self.low) & 0xFFF, mid: (!self.mid) & 0xFFF, high: (!self.high) & 0xFF }
    }

    pub fn rotr(self, n: u32) -> Word32 {
        Word32::from_u32(self.to_u32().rotate_right(n))
    }

    pub fn shr(self, n: u32) -> Word32 {
        Word32::from_u32(self.to_u32() >> n)
    }

    pub fn ch(x: Word32, y: Word32, z: Word32) -> Word32 {
        x.and(y).xor(x.not().and(z))
    }

    pub fn maj(x: Word32, y: Word32, z: Word32) -> Word32 {
        x.and(y).xor(x.and(z)).xor(y.and(z))
    }

    pub fn sigma0(x: Word32) -> Word32 {
        x.rotr(2).xor(x.rotr(13)).xor(x.rotr(22))
    }

    pub fn sigma1(x: Word32) -> Word32 {
        x.rotr(6).xor(x.rotr(11)).xor(x.rotr(25))
    }

    pub fn small_sigma0(x: Word32) -> Word32 {
        x.rotr(7).xor(x.rotr(18)).xor(x.shr(3))
    }

    pub fn small_sigma1(x: Word32) -> Word32 {
        x.rotr(17).xor(x.rotr(19)).xor(x.shr(10))
    }

    pub const fn zero() -> Self {
        Word32 { low: 0, mid: 0, high: 0 }
    }
}

impl Default for Word32 {
    fn default() -> Self {
        Self::zero()
    }
}

pub const K: [Word32; 64] = [
    Word32::from_u32(0x428A2F98), Word32::from_u32(0x71374491), Word32::from_u32(0xB5C0FBCF), Word32::from_u32(0xE9B5DBA5),
    Word32::from_u32(0x3956C25B), Word32::from_u32(0x59F111F1), Word32::from_u32(0x923F82A4), Word32::from_u32(0xAB1C5ED5),
    Word32::from_u32(0xD807AA98), Word32::from_u32(0x12835B01), Word32::from_u32(0x243185BE), Word32::from_u32(0x550C7DC3),
    Word32::from_u32(0x72BE5D74), Word32::from_u32(0x80DEB1FE), Word32::from_u32(0x9BDC06A7), Word32::from_u32(0xC19BF174),
    Word32::from_u32(0xE49B69C1), Word32::from_u32(0xEFBE4786), Word32::from_u32(0x0FC19DC6), Word32::from_u32(0x240CA1CC),
    Word32::from_u32(0x2DE92C6F), Word32::from_u32(0x4A7484AA), Word32::from_u32(0x5CB0A9DC), Word32::from_u32(0x76F988DA),
    Word32::from_u32(0x983E5152), Word32::from_u32(0xA831C66D), Word32::from_u32(0xB00327C8), Word32::from_u32(0xBF597FC7),
    Word32::from_u32(0xC6E00BF3), Word32::from_u32(0xD5A79147), Word32::from_u32(0x06CA6351), Word32::from_u32(0x14292967),
    Word32::from_u32(0x27B70A85), Word32::from_u32(0x2E1B2138), Word32::from_u32(0x4D2C6DFC), Word32::from_u32(0x53380D13),
    Word32::from_u32(0x650A7354), Word32::from_u32(0x766A0ABB), Word32::from_u32(0x81C2C92E), Word32::from_u32(0x92722C85),
    Word32::from_u32(0xA2BFE8A1), Word32::from_u32(0xA81A664B), Word32::from_u32(0xC24B8B70), Word32::from_u32(0xC76C51A3),
    Word32::from_u32(0xD192E819), Word32::from_u32(0xD6990624), Word32::from_u32(0xF40E3585), Word32::from_u32(0x106AA070),
    Word32::from_u32(0x19A4C116), Word32::from_u32(0x1E376C08), Word32::from_u32(0x2748774C), Word32::from_u32(0x34B0BCB5),
    Word32::from_u32(0x391C0CB3), Word32::from_u32(0x4ED8AA4A), Word32::from_u32(0x5B9CCA4F), Word32::from_u32(0x682E6FF3),
    Word32::from_u32(0x748F82EE), Word32::from_u32(0x78A5636F), Word32::from_u32(0x84C87814), Word32::from_u32(0x8CC70208),
    Word32::from_u32(0x90BEFFFA), Word32::from_u32(0xA4506CEB), Word32::from_u32(0xBEF9A3F7), Word32::from_u32(0xC67178F2),
];

pub const H_INIT: [Word32; 8] = [
    Word32::from_u32(0x6A09E667), Word32::from_u32(0xBB67AE85), Word32::from_u32(0x3C6EF372), Word32::from_u32(0xA54FF53A),
    Word32::from_u32(0x510E527F), Word32::from_u32(0x9B05688C), Word32::from_u32(0x1F83D9AB), Word32::from_u32(0x5BE0CD19),
];

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_from_u32() {
        let w = Word32::from_u32(0x12345678);
        assert_eq!(w.low, 0x678);
        assert_eq!(w.mid, 0x345);
        assert_eq!(w.high, 0x12);
    }

    #[test]
    fn test_to_u32() {
        let w = Word32 { low: 0x678, mid: 0x345, high: 0x12 };
        assert_eq!(w.to_u32(), 0x12345678);
    }

    #[test]
    fn test_add() {
        let a = Word32::from_u32(0x12345678);
        let b = Word32::from_u32(0x87654321);
        let (result, _carry) = a.add(b);
        assert_eq!(result.to_u32(), 0x99999999);
    }

    #[test]
    fn test_add_with_carry() {
        let a = Word32::from_u32(0xFFFFFFFF);
        let b = Word32::from_u32(1);
        let (result, carry) = a.add(b);
        assert_eq!(result.to_u32(), 0x00000000);
        assert!(carry);
    }

    #[test]
    fn test_rotr() {
        let w = Word32::from_u32(0x12345678);
        let rotated = w.rotr(4);
        assert_eq!(rotated.to_u32(), 0x81234567);
    }
}
