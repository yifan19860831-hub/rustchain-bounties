//! PDP-8 CPU Simulator

pub const MEMORY_SIZE: usize = 4096;

#[derive(Debug, Clone)]
pub struct PDP8CPU {
    pub ac: u16,
    pub pc: u16,
    pub l: bool,
    pub memory: [u16; MEMORY_SIZE],
    pub ir: u16,
}

impl PDP8CPU {
    pub fn new() -> Self {
        PDP8CPU { ac: 0, pc: 0, l: false, memory: [0; MEMORY_SIZE], ir: 0 }
    }

    pub fn read_memory(&self, addr: u16) -> u16 {
        self.memory[(addr as usize) & 0xFFF]
    }

    pub fn write_memory(&mut self, addr: u16, value: u16) {
        self.memory[(addr as usize) & 0xFFF] = value & 0xFFF;
    }

    pub fn step(&mut self) -> Result<(), String> {
        self.ir = self.read_memory(self.pc);
        self.pc = (self.pc + 1) & 0xFFF;
        
        let opcode = (self.ir >> 9) & 0b111;
        let _indirect = (self.ir & 0x0100) != 0;
        let _page = (self.ir & 0x0080) != 0;
        let offset = (self.ir & 0x007F) as u16;
        let ea = offset;

        match opcode {
            0b000 => self.ac &= self.read_memory(ea),
            0b001 => {
                let mem = self.read_memory(ea);
                let sum = (self.ac as u32) + (mem as u32) + (if self.l { 1 } else { 0 });
                self.l = (sum & 0x1000) != 0;
                self.ac = (sum as u16) & 0xFFF;
            }
            0b010 => {
                let mut val = self.read_memory(ea);
                val = (val + 1) & 0xFFF;
                self.write_memory(ea, val);
                if val == 0 {
                    self.pc = (self.pc + 1) & 0xFFF;
                }
            }
            0b011 => {
                self.write_memory(ea, self.ac);
                self.ac = 0;
            }
            0b100 => {
                self.write_memory(ea, self.pc);
                self.pc = (ea + 1) & 0xFFF;
            }
            0b101 => self.pc = ea,
            0b110 => {}
            0b111 => {
                if self.ir & 0x0100 != 0 { self.ac = 0; }
                if self.ir & 0x0200 != 0 { self.ac = (!self.ac) & 0xFFF; }
                if self.ir & 0x0001 != 0 { self.ac = (self.ac + 1) & 0xFFF; }
            }
            _ => {}
        }
        Ok(())
    }
}

impl Default for PDP8CPU {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cpu_basic() {
        let mut cpu = PDP8CPU::new();
        assert_eq!(cpu.ac, 0);
        assert_eq!(cpu.pc, 0);
        assert!(!cpu.l);
    }
}
