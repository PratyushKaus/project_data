"""
Assertion helpers for validating automotive test conditions.
"""
from typing import Union, Optional, Any, TypeVar

Number = TypeVar('Number', int, float)

def assert_signal_equal(actual: Any, expected: Any) -> None:
    """
    Assert that two signal values are equal.
    
    Args:
        actual: Actual signal value
        expected: Expected signal value
        
    Raises:
        AssertionError: If actual value does not match expected value
    """
    assert actual == expected, f"Expected {expected}, got {actual}"

def assert_signal_greater(actual: Number, threshold: Number) -> None:
    """
    Assert that a signal value is greater than a threshold.
    
    Args:
        actual: Actual signal value
        threshold: Minimum expected value
        
    Raises:
        AssertionError: If actual value is not greater than threshold
    """
    assert actual > threshold, f"Expected value > {threshold}, got {actual}"

def assert_signal_in_range(actual: Number, min_val: Number, max_val: Number) -> None:
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

def assert_speed_warning_threshold(speed: float, seatbelt_fastened: bool, warning_active: bool) -> None:
    """
    Assert that the warning system correctly responds to speed and seatbelt state.
    
    Args:
        speed: Current vehicle speed in km/h
        seatbelt_fastened: Whether seatbelt is fastened
        warning_active: Whether warning is currently active
        
    Raises:
        AssertionError: If warning state is incorrect for given speed and seatbelt state
    """
    SPEED_THRESHOLD = 10.0  # From test cases
    
    should_warn = speed > SPEED_THRESHOLD and not seatbelt_fastened
    assert warning_active == should_warn, \
        f"At {speed} km/h with seatbelt {'fastened' if seatbelt_fastened else 'unfastened'}, " \
        f"warning should be {'active' if should_warn else 'inactive'}"

def assert_engine_state(speed: float, engine_running: bool) -> None:
    """
    Assert that engine state is correct for the current speed.
    
    Args:
        speed: Current vehicle speed in km/h
        engine_running: Whether engine is currently running
        
    Raises:
        AssertionError: If engine state is incorrect for given speed
    """
    if speed > 0:
        assert engine_running, f"Engine should be running when speed is {speed} km/h"
