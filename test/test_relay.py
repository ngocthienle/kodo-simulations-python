#! /usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')

import unittest
import simulator.relay

class TestPacket(unittest.TestCase):

    def test_instantiation(self):
        id = "test_id"
        stats = {}
        decoder = "decoder_object"
        c = simulator.relay.Relay(id, stats, decoder)
        self.assertEqual(c.sender.id, id)
        self.assertEqual(c.receiver.id, id)
        self.assertEqual(c.receiver.decoder, decoder)

if __name__ == '__main__':
    unittest.main()