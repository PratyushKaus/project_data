"""
Assertion helpers for validating automotive test conditions.
"""

def assert_signal_equal(actual, expected):
    """
    Assert that two signal values are equal.
    
    :param actual: Actual signal value.
    :param expected: Expected signal value.
    """
    assert actual == expected, f"Expected {expected}, got {actual}"

def assert_signal_greater(actual, threshold):
    """
    Assert that a signal value is greater than a threshold.
    
    :param actual: Actual signal value.
    :param threshold: Minimum expected value.
    """
    assert actual > threshold, f"Expected value > {threshold}, got {actual}"

def assert_signal_in_range(actual, min_val, max_val):
    """
    Assert that a signal value is within a specified range.
    
    :param actual: Actual signal value.
    :param min_val: Minimum expected value.
    :param max_val: Maximum expected value.
    """
    assert min_val <= actual <= max_val, \
        f"Expected value in range [{min_val}, {max_val}], got {actual}"
