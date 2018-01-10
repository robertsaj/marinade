from components.abstract.controller import Controller
from components.abstract.ibus import iBusRead, iBusWrite

class ControllerSingleCycle(Controller):
    """

    """

    def __init__(self, cond, op, funct, rd, bit4, c, v, n, z, pcsrc, pcwr, regsa,
                regdst, regwrs, regwr, exts, alusrcb, alus, aluflagwr, memwr,
                regsrc, wd3s):
        """

        """

        # Input Buses
        if not isinstance(cond, iBusRead):
            raise TypeError('The cond bus must be readable')
        elif cond.size() != 4:
            raise ValueError('The cond bus must have a size of 4-bits')
        if not isinstance(op, iBusRead):
            raise TypeError('The op bus must be readable')
        elif op.size() != 2:
            raise ValueError('The op bus must have a size of 2-bits')
        if not isinstance(funct, iBusRead):
            raise TypeError('The funct bus must be readable')
        elif funct.size() != 6:
            raise ValueError('The funct bus must have a size of 6-bits')
        if not isinstance(rd, iBusRead):
            raise TypeError('The rd bus must be readable')
        elif rd.size() != 4:
            raise ValueError('The rd bus must have a size of 3-bits')
        if not isinstance(bit4, iBusRead):
            raise TypeError('The bit4 bus must be readable')
        elif bit4.size() != 1:
            raise ValueError('The bit4 bus must have a size of 1-bit')
        if not isinstance(c, iBusRead):
            raise TypeError('The c bus must be readable')
        elif c.size() != 1:
            raise ValueError('The c bus must have a size of 1-bit')
        if not isinstance(v, iBusRead):
            raise TypeError('The v bus must be readable')
        elif v.size() != 1:
            raise ValueError('The v bus must have a size of 1-bit')
        if not isinstance(n, iBusRead):
            raise TypeError('The n bus must be readable')
        elif n.size() != 1:
            raise ValueError('The n bus must have a size of 1-bit')
        if not isinstance(z, iBusRead):
            raise TypeError('The z bus must be readable')
        elif z.size() != 1:
            raise ValueError('The z bus must have a size of 1-bit')

        self._cond = cond
        self._op = op
        self._funct = funct
        self._rd = rd
        self._bit4 = bit4
        self._c = c
        self._v = v
        self._n = n
        self._z = z

        #Control output buses
        if not isinstance(pcsrc, iBusRead):
            raise TypeError('The pcsrc bus must be writable')
        elif pcsrc.size() != 2:
            raise ValueError('The pcsrc bus must have a size of 2-bits')
        if not isinstance(pcwr, iBusRead):
            raise TypeError('The pcwr bus must be writable')
        elif pcwr.size() != 1:
            raise ValueError('The pcwr bus must have a size of 1-bit')
        if not isinstance(regsa, iBusRead):
            raise TypeError('The regsa bus must be writable')
        elif regsa.size() != 1:
            raise ValueError('The regsa bus must have a size of 1-bit')
        if not isinstance(regdst, iBusRead):
            raise TypeError('The regdst bus must be writable')
        elif regdst.size() != 2:
            raise ValueError('The regdst bus must have a size of 2-bits')
        if not isinstance(regwrs, iBusRead):
            raise TypeError('The regwrs bus must be writable')
        elif regwrs.size() != 2:
            raise ValueError('The regwrs bus must have a size of 2-bits')
        if not isinstance(regwr, iBusRead):
            raise TypeError('The regwr bus must be writable')
        elif regwr.size() != 1:
            raise ValueError('The regwr bus must have a size of 1-bit')
        if not isinstance(exts, iBusRead):
            raise TypeError('The exts bus must be writable')
        elif exts.size() != 2:
            raise ValueError('The exts bus must have a size of 2-bits')
        if not isinstance(alusrcb, iBusRead):
            raise TypeError('The alusrcb bus must be writable')
        elif alusrcb.size() != 1:
            raise ValueError('The alusrcb bus must have a size of 1-bit')
        if not isinstance(alus, iBusRead):
            raise TypeError('The alus bus must be writable')
        elif alus.size() != 4:
            raise ValueError('The alus bus must have a size of 4-bits')
        if not isinstance(aluflagwr, iBusRead):
            raise TypeError('The aluflagwr bus must be writable')
        elif aluflagwr.size() != 1:
            raise ValueError('The aluflagwr bus must have a size of 1-bit')
        if not isinstance(memwr, iBusRead):
            raise TypeError('The memwr bus must be writable')
        elif memwr.size() != 1:
            raise ValueError('The memwr bus must have a size of 1-bit')
        if not isinstance(regsrc, iBusRead):
            raise TypeError('The regsrc bus must be writable')
        elif regsrc.size() != 1:
            raise ValueError('The regsrc bus must have a size of 1-bit')
        if not isinstance(wd3s, iBusRead):
            raise TypeError('The wd3s bus must be writable')
        elif wd3s.size() != 1:
            raise ValueError('The wd3s bus must have a size of 1-bit')

        self._pcsrc = pcsrc
        self._pcwr = pcwr
        self._regsa = regsa
        self._regdst = regdst
        self._regwrs = regwrs
        self._regwr = regwr
        self._exts = exts
        self._alusrcb = alusrcb
        self._alus = alus
        self._aluflagwr = aluflagwr
        self._memwr = memwr
        self._regsrc = regsrc
        self._wd3s = wd3s

    def _generate_pcsrc(op,cond,rd):
        if self._op.read() == 0b10 and (self._cond.read() == 0b110 or self._cond.read() == 0b0000 or self._cond.read() == 0b0001):
            self._pcsrc.write(0b00)
        elif self._op.read() == 0b00 and self._rd.read() == 0b1111:
            self._pcsrc.write(0b10)
        else:
            self._pcsrc.write(0b01)


    def run(self, time = None):
        ""

        # Read inputs
        op = self._op.read()
        funct = self._funct.read()
        bit4 = self._bit4.read()
        cond = self._cond.read()
        rd = self._rd.read()

        #Generate control outputs
        _generate_pcsrc(op,cond,rd)


        # pcwr - Always a 1 for the single cycle processor
        self._pcwr.write(0b1)

        #regsa
        if self._op.read() == 0b00 and self._bit4.read() == 0b1 and (self._funct.read() == 0b000000 or self._funct.read() == 0b000001):
            self._regsa.write(0b0)
        else:
            self._regsa.write(0b1)

        #regdst
        if self._op.read() == 0b01 and self._funct.read() == 0b011000:
            self._regdst.write(0b10)
        elif self._op.read() == 0b00 and self._bit4.read() == 0b1 and (self._funct.read() == 0b000000 or self._funct.read() == 0b000001):
            self._regdst.write(0b00)
        else:
            self._regdst.write(0b01)

        # regwrs
        if self._op.read() == 0b10 and ((self._funct.read() & 0b001000) >> 3) == 0b1:
            self._regwrs.write(0b10)
        elif self._op.read() == 0b00 and self._bit4.read() == 0b1 and (self._funct.read() == 0b000000 or self._funct.read() == 0b000001):
            self._regwrs.write(0b00)
        else:
            self._regwrs.write(0b01)

        # regwr
        if self._op.read() == 0b00 and (self._funct.read() == 0b010101 or self._funct.read() == 0b110101):
            self._regwr.write(0b0)
        elif self._op.read() == 0b01 and self._funct.read() == 0b011000:
            self._regwr.write(0b0)
        elif self._op.read() == 0b10 and ((self._funct.read() & 0b001000) >> 3) == 0b1:
            self._regwr.write(0b0)
        else:
            self._regwr.write(0b1)

        # exts
        if self._op.read() == 0b10:
            self._exts.write(0b10)
        elif self._op.read() == 0b01 and (self._funct.read() == 0b011000 or self._funct.read() == 0b011001):
            self._exts.write(0b01)
        else:
            self._exts.write(0b00)

        # alusrcb
        if self._op.read() == 0b00:
            if (self._funct.read() == 0b000000 or self._funct.read() == 0b000010 or
                    self._funct.read() == 0b000100 or self._funct.read() == 0b000110 or
                    self._funct.read() == 0b001000 or self._funct.read() == 0b001010 or
                    self._funct.read() == 0b001110 or self._funct.read() == 0b010001 or
                    self._funct.read() == 0b010011 or self._funct.read() == 0b010101 or
                    self._funct.read() == 0b010111 or self._funct.read() == 0b011000 or
                    self._funct.read() == 0b011000 or self._funct.read() == 0b011010 or
                    self._funct.read() == 0b011100 or self._funct.read() == 0b011110 or
                    self._funct.read() == 0b000001 or self._funct.read() == 0b000011 or
                    self._funct.read() == 0b000101 or self._funct.read() == 0b000111 or
                    self._funct.read() == 0b001001 or self._funct.read() == 0b001011 or
                    self._funct.read() == 0b011011 or self._funct.read() == 0b011101 or
                    self._funct.read() == 0b011111):
                self._alusrcb.write(0b1)
            elif self._bit4.read() == 0b1 and (self._funct.read() == 0b000000 or self._funct.read() == 0b000001):
                self._alusrcb.write(0b1)
            else:
                self._alusrcb.write(0b0)
        else:
            self._alusrcb.write(0b0)

        # alus
        if op == 0b00 and (funct == 0b000000 or 0b00 and funct == 0b000001) and bit4 == 0b1:
            self._alus.write(0b0111)
        elif op == 0b00 and (funct == 0b001000 or funct == 0b101000 or funct == 0b001001 or funct == 0b101001):
            self._alus.write(0b0000)
        elif op == 0b01 and (funct == 0b011000 or funct == 0b011001):
            self._alus.write(0b0000)
        elif op == 0b00 and (funct == 0b000100 or funct == 0b100100 or funct == 0b010101 or funct == 0b110101 or funct == 0b000101 or funct == 100101):
            self._alus.write(0b0001)
        elif op == 0b00 and (funct == 0b000000 or funct == 0b100000 or funct == 0b000001 or funct == 0b100001):
            self._alus.write(0b0010)
        elif op == 0b00 and (funct == 0b011000 or funct == 0b111000 or funct == 0b011001 or funct == 0b111001):
            self._alus.write(0b0011)
        elif op == 0b00 and (funct == 0b000010 or funct == 0b100010 or funct == 0b000011 or funct == 0b100011):
            self._alus.write(0b0100)
        elif op == 0b00 and (funct == 0b011010 or funct == 0b111010 or funct == 0b011011 or funct == 0b111011):
            self._alus.write(0b0110)
        else:
            self._alus.write(0b1111)


        # aluflagwr
        if self._op.read() == 0b00:
            # Note: need to look further into the logic when funct is 1
            if (self._funct.read() == 0b010101 or self._funct.read() == 0b110101 or
                    self._funct.read() == 0b000001 or self._funct.read() == 0b100001 or
                    self._funct.read() == 0b000011 or self._funct.read() == 0b100011 or
                    self._funct.read() == 0b000101 or self._funct.read() == 0b100101 or
                    self._funct.read() == 0b000111 or self._funct.read() == 0b100111 or
                    self._funct.read() == 0b001001 or self._funct.read() == 0b101001 or
                    self._funct.read() == 0b001011 or self._funct.read() == 0b101011 or
                    self._funct.read() == 0b001101 or self._funct.read() == 0b101101 or
                    self._funct.read() == 0b001111 or self._funct.read() == 0b101111 or
                    self._funct.read() == 0b010001 or self._funct.read() == 0b110001 or
                    self._funct.read() == 0b010011 or self._funct.read() == 0b110011 or
                    self._funct.read() == 0b010111 or self._funct.read() == 0b110111 or
                    self._funct.read() == 0b011001 or self._funct.read() == 0b111001 or
                    self._funct.read() == 0b011011 or self._funct.read() == 0b111011 or
                    self._funct.read() == 0b011101 or self._funct.read() == 0b111101 or
                    self._funct.read() == 0b011111 or self._funct.read() == 0b111111):
                self._aluflagwr.write(0b1)
            else:
                self._aluflagwr.write(0b0)
        else:
            self._aluflagwr.write(0b0)

        # memwr
        if self._op.read() == 0b01 and self._funct.read() == 0b011000:
            self._memwr.write(0b1)
        else:
            self._memwr.write(0b0)

        #regsrc
        if self._op.read() == 0b10 and self._funct.read() == 0b011001:
            self._regsrc.write(0b0)
        else:
            self._regsrc.write(0b1)

        #wd3s
        if self._op.read() == 0b10 and ((self._funct.read() & 0b001000) >> 3) == 0b1:
            self._wd3s.write(1)
        else:
            self._wd3s.write(0)


    def inspect(self):
        "Return message noting that this controller does not contain state"
        return {'type': 'sc-controller', 'state' : None}

    def modify(self, data=None):
        "Return message noting that this controller does not contain state"
        return {'error' : 'sc-controller does not contain state'}

    def on_rising_edge(self):
        "Not implemented for single cycle"
        pass

    def on_falling_edge(self):
        "Not implemented for single cycle"
        pass

    def on_reset(self):
        "Not implemented for single cycle"
        pass
