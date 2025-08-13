"""
Pytest fixtures for initializing and tearing down CANoe and dSPACE sessions.
"""
import pytest
from typing import Generator, Any
from baselib.canoe_utils import CanoeHandler
from baselib.dspace_utils import DspaceHandler

@pytest.fixture(scope="session")
def canoe() -> Generator[CanoeHandler, None, None]:
    """
    Session-scoped fixture for CANoe connection.
    Initializes CANoe, starts measurement, and ensures cleanup.
    
    Yields:
        CanoeHandler: Configured CANoe connection instance
    """
    canoe_instance = CanoeHandler(config_path="path/to/canoe/config")
    canoe_instance.start_measurement()
    yield canoe_instance
    canoe_instance.stop_measurement()

@pytest.fixture(scope="session")
def dspace() -> Generator[DspaceHandler, None, None]:
    """
    Session-scoped fixture for dSPACE connection.
    Initializes dSPACE, loads model, and ensures cleanup.
    
    Yields:
        DspaceHandler: Configured dSPACE connection instance
    """
    dspace_instance = DspaceHandler(model_path="path/to/dspace/model")
    dspace_instance.start_model()
    yield dspace_instance
    dspace_instance.stop_model()

@pytest.fixture(scope="function")
def test_setup(canoe: CanoeHandler, dspace: DspaceHandler) -> Generator[tuple[CanoeHandler, DspaceHandler], None, None]:
    """
    Function-scoped fixture for test setup and cleanup.
    Resets vehicle speed and seatbelt status before each test.
    
    Args:
        canoe: CANoe connection from session fixture
        dspace: dSPACE connection from session fixture
        
    Yields:
        tuple[CanoeHandler, DspaceHandler]: Tuple of configured test interfaces
    """
    # Reset vehicle state before test
    canoe.set_vehicle_speed(0.0)
    canoe.set_seatbelt_status(True)  # Seatbelt fastened by default
    dspace.simulate_vehicle_speed(0.0)
    dspace.simulate_seatbelt_state(True)
    dspace.wait_for_model_steady_state()
    
    yield canoe, dspace
    
    # Reset vehicle state after test
    canoe.set_vehicle_speed(0.0)
    canoe.set_seatbelt_status(True)
    dspace.simulate_vehicle_speed(0.0)
    dspace.simulate_seatbelt_state(True)
