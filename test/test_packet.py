#! /usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')

import unittest
import simulator.packet


class TestPacket(unittest.TestCase):
    """Class for testing Packet."""

    def test_instantiation(self):
        """Test instantiation."""
        sender = "sender object"
        data = "test_data"
        c = simulator.packet.Packet(sender, data)
        self.assertEqual(c.sender, sender)
        self.assertEqual(c.data, data)

if __name__ == '__main__':
    unittest.main()
