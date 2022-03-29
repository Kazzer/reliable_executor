#!/usr/bin/env python
"""Reliable executor for intermittently failing functions"""
import functools
import time


def reliably_execute(
        partial_function: functools.partial,
        *,
        retry: int=3,
        wait: int=5,
):
    """Helper function to reliably execute the provided partial function"""
    remaining_tries: int = retry + 1

    while remaining_tries > 0:
        remaining_tries -= 1
        try:
            return partial_function()
        # We catch Exception here because we don't know what kind it could be
        except Exception as exception:
            if remaining_tries:
                time.sleep(wait)
                continue
            raise RuntimeError(
                f'Could not reliably execute "{partial_function}" because of "{exception}"',
            )
