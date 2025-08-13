"""
Assertion helpers for validating automotive test conditions.
"""
from typing import Union, Optional

def assert_signal_equal(actual: Union[float, int, bool], expected: Union[float, int, bool]) -> None:
    """
    Assert that two signal values are equal.
    
    Args:
        actual: Actual signal value
        expected: Expected signal value
        
    Raises:
        AssertionError: If actual value does not match expected value
    """
    assert actual == expected, f"Expected {expected}, got {actual}"

def assert_signal_greater(actual: Union[float, int], threshold: Union[float, int]) -> None:
    """
    Assert that a signal value is greater than a threshold.
    
    Args:
        actual: Actual signal value
        threshold: Minimum expected value
        
    Raises:
        AssertionError: If actual value is not greater than threshold
    """
    assert actual > threshold, f"Expected value > {threshold}, got {actual}"

def assert_signal_in_range(actual: Union[float, int], min_val: Union[float, int], max_val: Union[float, int]) -> None:
    """
    Assert that a signal value is within a specified range.
    
    Args:
        actual: Actual signal value
        min_val: Minimum expected value
        max_val: Maximum expected value
        
    Raises:
        AssertionError: If actual value is not within the specified range
    """
    assert min_val <= actual <= max_val, \
        f"Expected value in range [{min_val}, {max_val}], got {actual}"

# Seatbelt Warning System Specific Assertions
def assert_chime_status(actual: bool, expected: bool, context: Optional[str] = None) -> None:
    """
    Assert that the warning chime status matches the expected state.
    
    Args:
        actual: Actual chime status (True for active, False for inactive)
        expected: Expected chime status
        context: Optional context message to include in assertion error
        
    Raises:
        AssertionError: If actual chime status does not match expected status
    """
    message = f"Expected chime {'active' if expected else 'inactive'}, got {'active' if actual else 'inactive'}"
    if context:
        message = f"{context}: {message}"
    assert actual == expected, message

def assert_speed_threshold(speed: float, threshold: float = 10.0) -> None:
    """
    Assert that the vehicle speed is above or below the warning threshold.
    
    Args:
        speed: Current vehicle speed in km/h
        threshold: Speed threshold for warning system (default 10.0 km/h)
        
    Raises:
        AssertionError: If speed is not in the correct range for the test
    """
    pass
