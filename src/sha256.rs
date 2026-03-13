//! SHA256 Implementation for PDP-8

use crate::arithmetic::{Word32, K, H_INIT};

pub const BLOCK_SIZE: usize = 64;
pub const DIGEST_SIZE: usize = 32;

pub struct SHA256 {
    h: [Word32; 8],
    buffer: [u8; BLOCK_SIZE],
    buffer_len: usize,
    length: u64,
}

impl SHA256 {
    pub fn new() -> Self {
        SHA256 { h: H_INIT, buffer: [0; BLOCK_SIZE], buffer_len: 0, length: 0 }
    }

    pub fn update(&mut self, data: &[u8]) {
        for &byte in data {
            self.buffer[self.buffer_len] = byte;
            self.buffer_len += 1;
            self.length += 8;
            if self.buffer_len == BLOCK_SIZE {
                self.process_block();
                self.buffer_len = 0;
            }
        }
    }

    pub fn finalize(mut self) -> [u8; DIGEST_SIZE] {
        let bit_len = self.length;
        let byte_len = self.buffer_len;
        self.buffer[byte_len] = 0x80;
        self.buffer_len = byte_len + 1;

        if self.buffer_len > 56 {
            while self.buffer_len < BLOCK_SIZE {
                self.buffer[self.buffer_len] = 0;
                self.buffer_len += 1;
            }
            self.process_block();
            self.buffer_len = 0;
        }

        while self.buffer_len < 56 {
            self.buffer[self.buffer_len] = 0;
            self.buffer_len += 1;
        }

        for i in 0..8 {
            self.buffer[56 + i] = ((bit_len >> (56 - i * 8)) & 0xFF) as u8;
        }

        self.process_block();

        let mut digest = [0u8; DIGEST_SIZE];
        for i in 0..8 {
            let word = self.h[i].to_u32();
            digest[i * 4 + 0] = ((word >> 24) & 0xFF) as u8;
            digest[i * 4 + 1] = ((word >> 16) & 0xFF) as u8;
            digest[i * 4 + 2] = ((word >> 8) & 0xFF) as u8;
            digest[i * 4 + 3] = (word & 0xFF) as u8;
        }
        digest
    }

    fn process_block(&mut self) {
        let mut w = [Word32::zero(); 64];

        for i in 0..16 {
            let offset = i * 4;
            let word = ((self.buffer[offset] as u32) << 24)
                | ((self.buffer[offset + 1] as u32) << 16)
                | ((self.buffer[offset + 2] as u32) << 8)
                | (self.buffer[offset + 3] as u32);
            w[i] = Word32::from_u32(word);
        }

        for i in 16..64 {
            w[i] = Word32::small_sigma1(w[i - 2])
                .add_wrapped(w[i - 7])
                .add_wrapped(Word32::small_sigma0(w[i - 15]))
                .add_wrapped(w[i - 16]);
        }

        let (mut a, mut b, mut c, mut d) = (self.h[0], self.h[1], self.h[2], self.h[3]);
        let (mut e, mut f, mut g, mut h) = (self.h[4], self.h[5], self.h[6], self.h[7]);

        for i in 0..64 {
            let t1 = h.add_wrapped(Word32::sigma1(e))
                .add_wrapped(Word32::ch(e, f, g))
                .add_wrapped(K[i])
                .add_wrapped(w[i]);
            let t2 = Word32::sigma0(a).add_wrapped(Word32::maj(a, b, c));
            h = g; g = f; f = e; e = d.add_wrapped(t1);
            d = c; c = b; b = a; a = t1.add_wrapped(t2);
        }

        self.h[0] = self.h[0].add_wrapped(a);
        self.h[1] = self.h[1].add_wrapped(b);
        self.h[2] = self.h[2].add_wrapped(c);
        self.h[3] = self.h[3].add_wrapped(d);
        self.h[4] = self.h[4].add_wrapped(e);
        self.h[5] = self.h[5].add_wrapped(f);
        self.h[6] = self.h[6].add_wrapped(g);
        self.h[7] = self.h[7].add_wrapped(h);
    }

    pub fn hash(data: &[u8]) -> [u8; DIGEST_SIZE] {
        let mut hasher = SHA256::new();
        hasher.update(data);
        hasher.finalize()
    }

    pub fn hash256(data: &[u8]) -> [u8; DIGEST_SIZE] {
        let first = Self::hash(data);
        Self::hash(&first)
    }
}

impl Default for SHA256 {
    fn default() -> Self {
        Self::new()
    }
}

pub fn digest_to_hex(digest: &[u8]) -> String {
    digest.iter().map(|b| format!("{:02x}", b)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sha256_empty() {
        let digest = SHA256::hash(b"");
        let hex = digest_to_hex(&digest);
        assert_eq!(hex, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
    }

    #[test]
    fn test_sha256_abc() {
        let digest = SHA256::hash(b"abc");
        let hex = digest_to_hex(&digest);
        assert_eq!(hex, "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
    }

    #[test]
    fn test_sha256_hello() {
        let digest = SHA256::hash(b"hello world");
        let hex = digest_to_hex(&digest);
        assert_eq!(hex, "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9");
    }
}
