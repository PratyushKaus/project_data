"""
High-level helper functions for engine-related tests.
"""
from typing import Optional, Tuple
from ..canoe_utils import CanoeHandler
from ..dspace_utils import DspaceHandler

def start_engine(canoe: CanoeHandler, dspace: DspaceHandler, target_rpm: float = 800.0) -> bool:
    """
    Start the engine and verify it reaches idle speed.
    
    Args:
        canoe: CANoe connection handler
        dspace: dSPACE connection handler
        target_rpm: Target idle RPM (default: 800.0)
        
    Returns:
        bool: True if engine started successfully, False otherwise
    """
    # Send engine start command using CAN message ID 291 (EngineState)
    canoe.send_message("EngineState", {
        "OnOff": 1,  # 1 = "On" from DBC value table
        "EngineSpeed": 0  # Initial speed
    })
    
    # Wait for engine to reach idle speed
    dspace.simulate_engine_start()
    
    # Verify engine speed stabilizes at target RPM
    for _ in range(10):  # Try for 1 second (100ms intervals)
        current_rpm = float(canoe.read_signal("EngineSpeed"))
        if abs(current_rpm - target_rpm) <= 50.0:  # Within 50 RPM tolerance
            return True
    return False

def stop_engine(canoe: CanoeHandler, dspace: DspaceHandler) -> bool:
    """
    Stop the engine and verify it comes to a complete stop.
    
    Args:
        canoe: CANoe connection handler
        dspace: dSPACE connection handler
        
    Returns:
        bool: True if engine stopped successfully, False otherwise
    """
    # Send engine stop command using CAN message ID 291 (EngineState)
    canoe.send_message("EngineState", {
        "OnOff": 0,  # 0 = "Off" from DBC value table
        "EngineSpeed": 0
    })
    
    # Simulate engine stop in dSPACE
    dspace.simulate_engine_stop()
    
    # Verify engine speed reaches 0
    for _ in range(10):  # Try for 1 second
        if float(canoe.read_signal("EngineSpeed")) == 0:
            return True
    return False

def verify_engine_running(canoe: CanoeHandler) -> Tuple[bool, float]:
    """
    Check if engine is running and get current RPM.
    
    Args:
        canoe: CANoe connection handler
        
    Returns:
        Tuple[bool, float]: (is_running, current_rpm)
            - is_running: True if engine is on and RPM > 0
            - current_rpm: Current engine speed in RPM
    """
    engine_state = canoe.read_signal("OnOff") == 1  # 1 = "On"
    current_rpm = float(canoe.read_signal("EngineSpeed"))
    return engine_state and current_rpm > 0, current_rpm
