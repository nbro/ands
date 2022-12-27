#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# Meta-info

Author: Nelson Brochado

Created: 21/01/2017

Updated: 04/08/2018

# Description

Unit tests for the functions in the ands.algorithms.recursion.factorial module.
"""

import math
import unittest
from random import randint

from ands.algorithms.recursion.factorial import *


class TestFactorial(unittest.TestCase):
    def test_factorial_0(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(iterative_factorial(0), 1)

    def test_factorial_1(self):
        self.assertEqual(factorial(1), 1)
        self.assertEqual(iterative_factorial(1), 1)

    def test_factorial_random_number(self):
        r = randint(2, 100)
        self.assertEqual(factorial(r), math.factorial(r))
        self.assertEqual(iterative_factorial(r), math.factorial(r))

    def test_multiple_factorial_0(self):
        self.assertEqual(multiple_factorial(0), [1])

    def test_multiple_factorial_1(self):
        self.assertEqual(multiple_factorial(1), [1, 1])

    def test_multiple_factorial_random_n(self):
        ls = []
        r = randint(2, 10)
        for i in range(r + 1):
            ls.append(math.factorial(i))
        self.assertEqual(multiple_factorial(r), ls)

    def test_smallest_geq_0(self):
        self.assertEqual(smallest_geq(0), 0)

    def test_smallest_geq_1(self):
        self.assertEqual(smallest_geq(1), 0)

    def test_smallest_geq_2(self):
        self.assertEqual(smallest_geq(2), 2)

    def test_smallest_geq_3(self):
        self.assertEqual(smallest_geq(3), 3)
