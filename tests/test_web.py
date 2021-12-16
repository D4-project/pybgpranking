#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from pybgpranking import PyBGPRanking


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.client = PyBGPRanking(root_url="https://bgpranking.circl.lu")

    def test_up(self):
        self.assertTrue(self.client.is_up)
        self.assertTrue(self.client.redis_up())
