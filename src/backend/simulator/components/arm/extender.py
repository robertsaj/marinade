"""
ARM Extender object for use in ARMv4 architectures

Configuration file template should follow form
{
    /* Required */

    "imm" : "",
    "exts" : "",
    "imm32" : ""
}

imm is data bus reference of 24 bits
exts is control bus reference
imm32 is 32 bit extended data bus reference
"""

from simulator.components.abstract.combinational import Combinational
from simulator.components.abstract.ibus import iBusRead, iBusWrite


class Extender(Combinational):
    """
    Extender object extends immediate field from instruction to word length for
    further manipulation by architecture
    """

    def __init__(self, imm, exts, imm32):
        """
        inputs:
            imm: 24-bit immediate
            exts: extender control signal
        output:
            imm32: resulting 32-bit immediate
        """

        if not isinstance(imm, iBusRead):
            raise TypeError('The imm bus must be readable')
        elif imm.size() != 24:
            raise ValueError('The imm bus must have a size of 24-bits')
        if not isinstance(exts, iBusRead):
            raise TypeError('The exts bus must be readable')
        elif exts.size() != 2:
            raise ValueError('The exts bus must have a size of 2-bits')
        if not isinstance(imm32, iBusWrite):
            raise TypeError('The imm32 bus must be writable')
        elif imm32.size() != 32:
            raise ValueError('The imm32 bus must have a size of 32-bits')
        self._imm = imm
        self._exts = exts
        self._imm32 = imm32

    def run(self, time=None):
        """
        exts = 0 for data processing instructions
        exts = 1 for load and store instructions
        exts = 2 or 3 for branch instructions
        """

        # keep only the 8 most least significant bits and rotate by field
        if self._exts.read() == 0:
            rotate = (self._imm.read() & 0x00000F00) >> 8
            imm = self._imm.read() & 0x000000FF
            for i in range(0,rotate):
                t1 = imm & 0x1
                t2 = (imm & 0x2) >> 1
                imm = (imm >> 2) | (t1 << 30) | (t2 << 31)
            self._imm32.write(imm & (2**32 - 1))
        # keep only the 12 most least significant bits
        elif self._exts.read() == 1:
            self._imm32.write(self._imm.read() & 0x00000FFF)
        else:
            # sign extend the immediate and add put 0's in the 2 least significant bits
            new_imm = self._imm.read()
            signed_bit = (0x800000 & new_imm) >> 23
            if signed_bit == 1:
                new_imm = 0x3F000000 | new_imm
            self._imm32.write(new_imm << 2)

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"
        return Extender(hooks[config["imm"]],hooks[config["exts"]],
                        hooks[config["imm32"]])
