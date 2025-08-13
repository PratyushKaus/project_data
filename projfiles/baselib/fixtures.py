"""
Pytest fixtures for initializing and tearing down CANoe and dSPACE sessions.
"""

import pytest
from baselib.canoe_utils import CanoeHandler
from baselib.dspace_utils import DspaceHandler

@pytest.fixture(scope="session")
def canoe():
    """
    Session-scoped fixture for CANoe connection.
    Adjust the config_path as needed for your environment.
    """
    canoe_instance = CanoeHandler(config_path="path/to/canoe/config")
    canoe_instance.start_measurement()
    yield canoe_instance
    canoe_instance.stop_measurement()

@pytest.fixture(scope="session")
def dspace():
    """
    Session-scoped fixture for dSPACE connection.
    Adjust the model_path as needed for your environment.
    """
    dspace_instance = DspaceHandler(model_path="path/to/dspace/model")
    yield dspace_instance
    dspace_instance.stop_model()
