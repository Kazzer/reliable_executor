#!/usr/bin/env python
"""Reliable executor for intermittently failing functions"""
import time


def reliably_execute(
        function,
        *args,
        **kwargs
):
    """Helper function to reliably execute the provided function"""
    if 'reliable_retry' in kwargs.keys():
        reliable_retry = kwargs.pop('reliable_retry')
    else:
        reliable_retry = 3

    if 'reliable_wait' in kwargs.keys():
        reliable_wait = kwargs.pop('reliable_wait')
    else:
        reliable_wait = 5

    remaining_tries = reliable_retry + 1

    while remaining_tries > 0:
        remaining_tries -= 1
        try:
            return function(*args, **kwargs)
        # We catch Exception here because we don't know what kind it could be
        except Exception as exception:
            if remaining_tries:
                time.sleep(reliable_wait)
                continue
            raise RuntimeError(
                'Could not reliably execute "{}" because of "{}"'
                .format(function, exception)
            )
