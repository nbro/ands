#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# Meta info

Author: Nelson Brochado

Created: 17/02/2016

Updated: 12/03/2017

# Description

Unit tests for the MaxHeap class.
"""

import unittest
from random import randint, choice, sample

from ands.ds.MaxHeap import MaxHeap


class TestMaxHeap(unittest.TestCase):
    def test_heap_creation_default(self):
        h = MaxHeap()
        self.assertTrue(h.is_empty())
        self.assertEqual(h.size(), 0)

    def test_heap_creation_given_list(self):
        a = [12, 14, 28, 6, 7, 10, 18]
        h = MaxHeap(a)
        self.assertFalse(h.is_empty())
        self.assertEqual(h.size(), len(a))

    def test_clear_empty_heap(self):
        h = MaxHeap()
        self.assertIsNone(h.clear())
        self.assertEqual(h.size(), 0)
        self.assertTrue(h.is_empty())

    def test_clear_heap_of_random_size(self):
        h = MaxHeap([randint(-100, 100) for _ in range(100)])
        self.assertIsNone(h.clear())
        self.assertEqual(h.size(), 0)
        self.assertTrue(h.is_empty())

    def test_add_when_argument_is_None(self):
        h = MaxHeap()
        self.assertRaises(ValueError, h.add, None)

    def test_add_add_one(self):
        h = MaxHeap()
        self.assertIsNone(h.add(2))
        self.assertEqual(h.size(), 1)
        self.assertFalse(h.is_empty())
        self.assertEqual(h.find_max(), 2)

    def test_add_multiple_elements(self):
        a = [randint(-100, 100) for _ in range(100)]
        h = MaxHeap()

        for i, elem in enumerate(a):
            self.assertIsNone(h.add(elem))
            self.assertEqual(h.size(), i + 1)

        self.assertFalse(h.is_empty())
        self.assertEqual(h.find_max(), max(a))

    def test_contains_when_argument_is_None(self):
        h = MaxHeap()
        self.assertRaises(ValueError, h.contains, None)

    def test_contains_when_empty_heap(self):
        h = MaxHeap()
        self.assertFalse(h.contains(3))

    def test_contains_true(self):
        h = MaxHeap([6, 8, 2, 2, 60, 7, 9])
        self.assertTrue(h.contains(2))

    def test_contains_false(self):
        h = MaxHeap([6, 8, 2, 60, 7, 9, 3, 67])
        self.assertFalse(h.contains(10))

    def test_delete_when_argument_is_None(self):
        self.assertRaises(ValueError, MaxHeap().delete, None)

    def test_delete_when_elem_does_not_exist(self):
        self.assertRaises(LookupError, MaxHeap().delete, 3)

    def test_delete_when_elem_is_last(self):
        h = MaxHeap([3, 4])
        self.assertIsNone(h.delete(4))
        self.assertEqual(h.size(), 1)
        self.assertFalse(h.is_empty())

    def test_delete_all_when_heap_of_random_size(self):
        size = randint(3, 100)
        a = [randint(-100, 100) for _ in range(size)]
        h = MaxHeap(a)

        for _ in range(size):
            self.assertIsNone(h.delete(choice(a)))

        self.assertEqual(h.size(), 0)
        self.assertTrue(h.is_empty())

    def test_find_max_when_empty_heap(self):
        h = MaxHeap()
        self.assertIsNone(h.find_max())

    def test_find_max_when_heap_has_size_1(self):
        h = MaxHeap([5])
        self.assertEqual(h.find_max(), 5)

    def test_find_max_when_heap_has_size_2(self):
        h = MaxHeap([13, 7])
        self.assertEqual(h.find_max(), 13)

    def test_find_max_when_heap_has_random_size(self):
        a = [randint(-100, 100) for _ in range(3, 100)]
        h = MaxHeap(a)
        self.assertEqual(h.find_max(), max(a))

    def test_remove_max_when_empty_heap(self):
        h = MaxHeap()
        self.assertIsNone(h.remove_max())

    def test_remove_max_when_heap_has_size_1(self):
        h = MaxHeap([13])
        self.assertEqual(h.remove_max(), 13)
        self.assertTrue(h.is_empty())
        self.assertEqual(h.size(), 0)

    def test_remove_max_when_heap_has_size_2(self):
        h = MaxHeap([11, 13])
        self.assertEqual(h.remove_max(), 13)
        self.assertFalse(h.is_empty())
        self.assertEqual(h.size(), 1)

    def test_remove_max_when_heap_has_random_size(self):
        size = randint(3, 100)
        a = [randint(-100, 100) for _ in range(size)]
        h = MaxHeap(a)
        m = max(a)
        self.assertEqual(h.remove_max(), m)
        self.assertFalse(h.is_empty())
        self.assertEqual(h.size(), size - 1)

    def test_merge_empty_heap_with_empty_heap(self):
        a = MaxHeap()
        b = MaxHeap()
        self.assertIsNone(a.merge(b))

    def test_merge_empty_heap_with_non_empty_heap(self):
        a = MaxHeap()
        ls = [-3, 5, 7, 9, 1, 5, 2]
        b = MaxHeap(ls)
        self.assertIsNone(a.merge(b))
        self.assertEqual(a.size(), len(ls))
        self.assertEqual(b.size(), len(ls))

    def test_merge_non_empty_heap_with_empty_heap(self):
        ls = [-3, 5, 7, 9, 1, 5, 2]
        a = MaxHeap(ls)
        b = MaxHeap()
        self.assertIsNone(a.merge(b))
        self.assertEqual(a.size(), len(ls))
        self.assertEqual(b.size(), 0)
        self.assertTrue(b.is_empty())

    def test_merge_non_empty_heap_with_non_empty_heap(self):
        ls = [-3, 5, 7, 9, 1, 5, 2]
        size = len(ls)
        a = MaxHeap(ls)
        b = MaxHeap(sample(ls, size))
        self.assertIsNone(a.merge(b))
        self.assertEqual(a.size(), size * 2)
        self.assertEqual(b.size(), size)
