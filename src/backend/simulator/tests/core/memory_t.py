"""
Test core component Memory
"""

from collections import OrderedDict
import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.core.memory import Memory, Latch_Type, Logic_States
from simulator.components.core.constant import Constant
from simulator.components.core.bus import Bus
import simulator.limits as limits


class Memory_t(unittest.TestCase):
    """
    Test Core Memory constructor, inspect, modify, clocking, reset, and run
    functionality.
    """

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        clk = Bus(1, 0)
        rst = Bus(1, 0)
        a = Bus(8, 0)
        w = Bus(16, 0)
        r = Bus(16, 0)
        en = Bus(1, 0)
        accessMode = Bus(2, 3)

        # Test configuration parameters
        with self.assertRaises(TypeError):
            mem = Memory(17.1, 2, 0, a, w, en, rst, clk, accessMode, r)

        with self.assertRaises(ValueError):
            mem = Memory(limits.MAX_MEMORY_BLOCK + 1, 2, 0, a, w, en, rst, clk, accessMode, r)

        with self.assertRaises(TypeError):
            mem = Memory(256, 'v', 0, a, w, en, rst, clk, r)

        with self.assertRaises(ValueError):
            mem = Memory(256, limits.MAX_BYTES_IN_WORD + 1, 0, a, w, en, rst, clk, accessMode, r)

        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r, default_value='cake')

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r, default_value=2**(8 * 2))

        with self.assertRaises(TypeError):
            mem = Memory(256, 2, [], a, w, en, rst, clk, accessMode, r)

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, limits.MAX_ADDRESS + 1, a, w, en, rst, clk, accessMode, r)

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, limits.MAX_ADDRESS + 1 - 256, a, w, en, rst, clk, accessMode, r)

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r, edge_type=None)

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r, reset_type='cats')

        with self.assertRaises(ValueError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r, writeEnable_type=[])

        # Test bus parameters
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, 'a', w, en, rst, clk, accessMode, r)

        with self.assertRaises(ValueError):
            a = Bus(7)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r)

        a = Bus(8)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, 'w', en, rst, clk, accessMode, r)

        with self.assertRaises(ValueError):
            w = Bus(17)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r)

        w = Bus(16)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, 'en', rst, clk, accessMode, r)

        with self.assertRaises(ValueError):
            en = Bus(2)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r)

        en = Bus(1)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, en, 'rst', clk, accessMode, r)

        with self.assertRaises(ValueError):
            rst = Bus(2)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r)

        rst = Bus(1)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, en, rst, 'clk', accessMode, r)

        with self.assertRaises(ValueError):
            clk = Bus(2)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r)

        clk = Bus(1)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, 'accessMode', r)

        with self.assertRaises(ValueError):
            accessMode = Bus(1)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r)

        accessMode = Bus(2)
        with self.assertRaises(TypeError):
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, 'r')

        with self.assertRaises(ValueError):
            r = Bus(15)
            mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r)

        r = Bus(16)

        # Construct a valid object
        mem = Memory(256, 2, 0, a, w, en, rst, clk, accessMode, r, 0, Latch_Type.FALLING_EDGE,
                     Logic_States.ACTIVE_LOW, Logic_States.ACTIVE_LOW)

    def test_access_modes(self):
        """
        Tests and validates the different read/write modes for general memory
        """
        a = Bus(10)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        accessMode = Bus(2, 0)

        # 32-bit memory words
        wd = Bus(32)
        rd = Bus(32)
        mem = Memory(1024, 4, 0, a, wd, memwr, reset, clock, accessMode, rd)

        accessMode.write(3)
        a.write(0)
        wd.write(0xFFFFFFFF)
        memwr.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(msg['state'][0], 0xFF)
        self.assertEqual(msg['state'][1], 0xFF)
        self.assertEqual(msg['state'][2], 0xFF)
        self.assertEqual(msg['state'][3], 0xFF)

        wd = Bus(32)
        rd = Bus(32)
        mem = Memory(1024, 4, 0, a, wd, memwr, reset, clock, accessMode, rd)

        accessMode.write(0)
        a.write(0)
        wd.write(0xFFFFFFFF)
        memwr.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(len(msg['state'].keys()), 0)

        # 24-bit memory words
        wd = Bus(24)
        rd = Bus(24)
        mem = Memory(1024, 3, 0, a, wd, memwr, reset, clock, accessMode, rd, default_value=0)

        accessMode.write(3)
        a.write(0)
        wd.write(0xFFFFFF)
        memwr.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(msg['state'][0], 0xFF)
        self.assertEqual(msg['state'][1], 0xFF)
        self.assertEqual(msg['state'][2], 0xFF)

        wd = Bus(24)
        rd = Bus(24)
        mem = Memory(1024, 3, 0, a, wd, memwr, reset, clock, accessMode, rd, default_value=0)

        accessMode.write(2)
        a.write(0)
        wd.write(0xFFFFFF)
        memwr.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(msg['state'][0], 0xFF)
        self.assertEqual(len(msg['state'].keys()), 1)

        # 16-bit memory words
        wd = Bus(16)
        rd = Bus(16)
        mem = Memory(1024, 2, 0, a, wd, memwr, reset, clock, accessMode, rd)

        accessMode.write(2)
        a.write(0)
        wd.write(0xFFFF)
        memwr.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(msg['state'][0], 0xFF)
        self.assertEqual(len(msg['state'].keys()), 1)

        wd = Bus(16)
        rd = Bus(16)
        mem = Memory(1024, 2, 0, a, wd, memwr, reset, clock, accessMode, rd)

        accessMode.write(1)
        a.write(0)
        wd.write(0xFFFF)
        memwr.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(msg['state'][0], 0xFF)
        self.assertEqual(len(msg['state'].keys()), 1)

        # 8-bit memory words
        wd = Bus(8)
        rd = Bus(8)
        mem = Memory(1024, 1, 0, a, wd, memwr, reset, clock, accessMode, rd)

        accessMode.write(1)
        a.write(0)
        wd.write(0xFF)
        memwr.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(msg['state'][0], 0xFF)
        self.assertEqual(len(msg['state'].keys()), 1)

        wd = Bus(8)
        rd = Bus(8)
        mem = Memory(1024, 1, 0, a, wd, memwr, reset, clock, accessMode, rd)

        accessMode.write(0)
        a.write(0)
        wd.write(0xFF)
        memwr.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(len(msg['state'].keys()), 0)

        wd = Bus(8)
        rd = Bus(8)
        mem = Memory(1024, 1, 0, a, wd, memwr, reset, clock, accessMode, rd)

        accessMode.write(2)  # half of byte is invalid since min is bytes (so off)
        a.write(0)
        wd.write(0xFF)
        memwr.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(len(msg['state'].keys()), 0)

        wd = Bus(8)
        rd = Bus(8)
        mem = Memory(1024, 1, 0, a, wd, memwr, reset, clock, accessMode, rd)

        accessMode.write(3)
        a.write(0)
        wd.write(0xFF)
        memwr.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(msg['state'][0], 0xFF)
        self.assertEqual(len(msg['state'].keys()), 1)

    def test_on_rising_edge(self):
        """
        tests the memory's on_rising_edge function
        """
        clk = Bus(1, 0)
        rst = Bus(1, 0)
        a = Bus(10, 0)
        w = Bus(32, 10)
        r = Bus(32, 0)
        en = Bus(1, 1)
        accessMode = Bus(2, 3)

        mem = Memory(1024, 4, 0, a, w, en, rst, clk, accessMode, r,
                     default_value=55, edge_type=Latch_Type.FALLING_EDGE)
        mem.on_rising_edge()
        self.assertTrue(0 not in mem.inspect()['state'])

        mem = Memory(1024, 4, 0, a, w, en, rst, clk, accessMode, r,
                     default_value=55, edge_type=Latch_Type.RISING_EDGE)
        mem.on_rising_edge()
        self.assertTrue(0 in mem.inspect()['state'])
        self.assertEqual(mem.inspect()['state'][3], 10)

    def test_on_falling_edge(self):
        """
        tests the memory's on_falling_edge function
        """
        clk = Bus(1, 0)
        rst = Bus(1, 0)
        a = Bus(10, 0)
        w = Bus(32, 10)
        r = Bus(32, 0)
        en = Bus(1, 1)
        accessMode = Bus(2, 3)

        mem = Memory(1024, 4, 0, a, w, en, rst, clk, accessMode, r,
                     default_value=55, edge_type=Latch_Type.RISING_EDGE)
        mem.on_falling_edge()
        self.assertTrue(0 not in mem.inspect()['state'])

        mem = Memory(1024, 4, 0, a, w, en, rst, clk, accessMode, r,
                     default_value=55, edge_type=Latch_Type.FALLING_EDGE)
        mem.on_falling_edge()
        self.assertTrue(0 in mem.inspect()['state'])
        self.assertEqual(mem.inspect()['state'][3], 10)

    def test_on_reset(self):
        """
        tests the memory's on reset function
        """
        a = Bus(10)
        wd = Bus(32)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(32)
        accessMode = Bus(2, 3)

        mem = Memory(1024, 4, 0, a, wd, memwr, reset, clock, accessMode, rd)

        a.write(0x0)
        wd.write(1)
        mem.on_falling_edge()
        a.write(0xC)
        wd.write(1)
        mem.on_falling_edge()

        msg = mem.inspect()
        self.assertEqual(len(msg['state'].keys()), 8)
        mem.on_reset()
        msg = mem.inspect()
        self.assertEqual(len(msg['state'].keys()), 0)

    def test_inspect(self):
        """
        Tests the memory's insect function
        """
        a = Bus(10)
        wd = Bus(8)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(8)
        accessMode = Bus(2, 3)

        mem = Memory(1024, 1, 4, a, wd, memwr, reset, clock, accessMode, rd)
        msg = mem.inspect()
        self.assertEqual(msg['type'], 'Memory')
        self.assertEqual(msg['size'], 1024)
        self.assertEqual(len(msg['state'].keys()), 0)

        a.write(0x4)
        wd.write(1)
        mem.on_falling_edge()
        a.write(0xC)
        wd.write(201)
        mem.on_falling_edge()

        msg = mem.inspect()
        self.assertEqual(msg['type'], 'Memory')
        self.assertEqual(msg['size'], 1024)
        self.assertEqual(len(msg['state'].keys()), 2)
        self.assertEqual(msg['state'][0x4], 1)
        self.assertEqual(msg['state'][0xC], 201)

    def test_modify(self):
        """
        tests the memory's modify function
        """
        a = Bus(1)
        wd = Bus(8)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(8)
        accessMode = Bus(2, 3)

        mem = Memory(2, 1, 0, a, wd, memwr, reset, clock, accessMode, rd)

        tm = None
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {}
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': '0',
            'data': []
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': -1,
            'data': []
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 2,
            'data': []
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 0,
            'data': '[]'
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 1,
            'data': [12, 15]
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 0,
            'data': [12, 15, 25]
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 0,
            'data': [256]
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 0,
            'data': [256, 256]
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

        tm = {
            'start': 0,
            'data': [255, 255]
        }
        rm = mem.modify(tm)
        self.assertTrue('success' in rm)

        tm = {
            'start': 0,
            'data': [15]
        }
        rm = mem.modify(tm)
        self.assertTrue('success' in rm)

        tm = {
            'start': 1,
            'data': [25]
        }
        rm = mem.modify(tm)
        self.assertTrue('success' in rm)

        tm = {
            'start': 0,
            'data': []
        }
        rm = mem.modify(tm)
        self.assertTrue('error' in rm)

    def test_run(self):
        """
        tests the memory's run function
        """
        a = Bus(2)
        wd = Bus(8)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(8)
        accessMode = Bus(2, 3)

        mem = Memory(3, 1, 0, a, wd, memwr, reset, clock, accessMode, rd, default_value=37)

        # write to each memory address
        memwr.write(1)
        for i in range(0, 4):
            a.write(i)
            wd.write(i * 25)
            clock.write(0)
            mem.run()
            clock.write(1)
            mem.run()
            clock.write(0)
            mem.run()

        # read from each valid memory address
        memwr.write(0)
        for i in range(0, 3):
            a.write(i)
            mem.run()
            self.assertEqual(rd.read(), i * 25)

        # read from invalid memory address
        a.write(3)
        mem.run()
        self.assertEqual(rd.read(), 37)

    def test_clear(self):
        "Tests memory's clear method"
        a = Bus(2)
        wd = Bus(8)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(8)
        accessMode = Bus(2, 3)

        mem = Memory(3, 1, 0, a, wd, memwr, reset, clock, accessMode, rd, default_value=37)

        # write memory
        mem.modify({'start': 0, 'data': [55]})
        msg = mem.inspect()
        self.assertNotEqual(len(msg['state'].keys()), 0)

        # clear and prove empty
        msg = mem.clear()
        self.assertTrue('success' in msg)

        msg = mem.inspect()
        self.assertEqual(len(msg['state'].keys()), 0)

    def test_from_dict(self):
        "Validates dictionary constructor"
        hooks = OrderedDict({
            "wr" : Bus(32),
            "en" : Bus(1),
            "addr" : Bus(6),
            "rst" : Bus(1),
            "clk" : Bus(1),
            "mode" : Bus(2),
            "rd" : Bus(32)
        })

        config = {
            "size" : 64,
            "bytes_per_word" : 4,
            "start_address" : 0,
            "address" : "addr",
            "write" : "wr",
            "enable" : "en",
            "reset" : "rst",
            "clock" : "clk",
            "access_mode" : "mode",
            "read" : "rd",
            "value" : 55,
            "edge_type" : "rising_edge",
            "reset_type" : "active_high",
            "enable_type" : "active_high"
        }

        mem = Memory.from_dict(config,hooks)


if __name__ == '__main__':
    unittest.main()
