#!/usr/bin/env python
"""Tests for the reliable_executor module"""
import random
import unittest

import reliable_executor


class ReliablyExecuteTest(unittest.TestCase):
    """Test Case for reliable_executor.reliably_execute()"""

    def setUp(self):
        """Sets up a function with a random number of fails before success"""
        self.number_of_fails = random.randint(1, 4)

    def intermittent_result(self, number_of_fails=0):
        """An intermittently failing function"""
        remaining_fails = number_of_fails

        while remaining_fails:
            yield UserWarning('Failing result')
            remaining_fails -= 1

        yield 0

    def intermittent_function(self, generator):
        """A function that will fail intermittently"""
        result = next(generator)

        if isinstance(result, Exception):
            raise result

        return result

    def test_success_without_failures(self):
        """Tests that the correct result is returned if the function doesn't fail"""
        result = reliable_executor.reliably_execute(
            self.intermittent_function,
            self.intermittent_result(),
            reliable_retry=0,
            reliable_wait=0,
        )

        self.assertEqual(result, 0)

    def test_success_with_failures(self):
        """Tests that the correct result is returned if the function fails"""
        result = reliable_executor.reliably_execute(
            self.intermittent_function,
            self.intermittent_result(self.number_of_fails),
            reliable_retry=self.number_of_fails,
            reliable_wait=0,
        )

        self.assertEqual(result, 0)

    def test_failure(self):
        """Tests that an exception is raised if the function doesn't succeed"""
        with self.assertRaises(RuntimeError):
            reliable_executor.reliably_execute(
                self.intermittent_function,
                self.intermittent_result(self.number_of_fails),
                reliable_retry=(self.number_of_fails - 1),
                reliable_wait=0,
            )
