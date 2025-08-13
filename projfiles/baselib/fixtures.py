"""
Pytest fixtures for initializing and tearing down CANoe and dSPACE sessions.
"""
from typing import Generator, Any, Tuple
import pytest
from pathlib import Path
import os
import logging

from baselib.canoe_utils import CanoeHandler
from baselib.dspace_utils import DspaceHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def test_config() -> dict:
    """
    Session-scoped fixture providing test configuration.
    
    Returns:
        dict: Configuration parameters for the test environment
    """
    return {
        "canoe_config": os.getenv("CANOE_CONFIG", "path/to/canoe/config"),
        "dspace_model": os.getenv("DSPACE_MODEL", "path/to/dspace/model"),
        "speed_threshold": 10.0,  # km/h
        "warning_timeout": 1.0,   # seconds
    }

@pytest.fixture(scope="session")
def canoe(test_config: dict) -> Generator[CanoeHandler, None, None]:
    """
    Session-scoped fixture for CANoe connection.
    Initializes CANoe and ensures proper cleanup.
    
    Args:
        test_config: Test configuration dictionary
        
    Yields:
        CanoeHandler: Configured CANoe connection instance
    """
    logger.info("Initializing CANoe connection...")
    canoe_instance = CanoeHandler(config_path=test_config["canoe_config"])
    
    try:
        canoe_instance.start_measurement()
        logger.info("CANoe measurement started")
        yield canoe_instance
    finally:
        logger.info("Stopping CANoe measurement...")
        canoe_instance.stop_measurement()

@pytest.fixture(scope="session")
def dspace(test_config: dict) -> Generator[DspaceHandler, None, None]:
    """
    Session-scoped fixture for dSPACE connection.
    Initializes dSPACE and ensures proper cleanup.
    
    Args:
        test_config: Test configuration dictionary
        
    Yields:
        DspaceHandler: Configured dSPACE connection instance
    """
    logger.info("Initializing dSPACE connection...")
    dspace_instance = DspaceHandler(model_path=test_config["dspace_model"])
    
    try:
        dspace_instance.start_model()
        logger.info("dSPACE model started")
        yield dspace_instance
    finally:
        logger.info("Stopping dSPACE model...")
        dspace_instance.stop_model()

@pytest.fixture(scope="function")
def test_setup(
    canoe: CanoeHandler,
    dspace: DspaceHandler,
    test_config: dict
) -> Generator[Tuple[CanoeHandler, DspaceHandler], None, None]:
    """
    Function-scoped fixture for test setup and cleanup.
    Resets vehicle state before and after each test.
    
    Args:
        canoe: CANoe connection from session fixture
        dspace: dSPACE connection from session fixture
        test_config: Test configuration dictionary
        
    Yields:
        Tuple[CanoeHandler, DspaceHandler]: Tuple of configured test interfaces
    """
    logger.info("Setting up test environment...")
    
    # Reset vehicle state before test
    canoe.set_vehicle_speed(0.0)
    canoe.set_seatbelt_status(True)  # Seatbelt fastened by default
    dspace.simulate_vehicle_speed(0.0)
    dspace.simulate_seatbelt_state(True)
    
    # Wait for model to stabilize
    dspace.wait_for_model_steady_state()
    
    yield canoe, dspace
    
    logger.info("Cleaning up test environment...")
    
    # Reset vehicle state after test
    canoe.set_vehicle_speed(0.0)
    canoe.set_seatbelt_status(True)
    dspace.simulate_vehicle_speed(0.0)
    dspace.simulate_seatbelt_state(True)
    
    # Additional cleanup if needed
    dspace.wait_for_model_steady_state()
