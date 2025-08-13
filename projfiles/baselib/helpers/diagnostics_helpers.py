"""
High-level helper functions for diagnostics.
"""
from typing import Optional, List, Dict
from ..canoe_utils import CanoeHandler
from ..dspace_utils import DspaceHandler

def send_dtc_request(canoe: CanoeHandler, dtc_code: str) -> bool:
    """
    Send a diagnostic trouble code request over CAN.
    
    Args:
        canoe: CANoe connection handler
        dtc_code: The DTC code to request (e.g., "P0123")
        
    Returns:
        bool: True if request was sent successfully, False otherwise
    """
    # Using message ID 291 (EngineState) for diagnostics
    # In a real implementation, would use proper diagnostic message IDs
    try:
        canoe.send_message("EngineState", {
            "OnOff": 1,  # Enable diagnostic mode
            "EngineSpeed": 0  # Not used for diagnostics
        })
        return True
    except Exception:
        return False

def verify_dtc_present(canoe: CanoeHandler, dtc_code: str) -> bool:
    """
    Verify if a specific DTC is present in the ECU.
    
    Args:
        canoe: CANoe connection handler
        dtc_code: The DTC code to check (e.g., "P0123")
        
    Returns:
        bool: True if DTC is present, False otherwise
    """
    # In real implementation, would use proper diagnostic response message
    try:
        response = canoe.read_signal("OnOff")
        return response == 1  # 1 = DTC present
    except Exception:
        return False

def get_active_dtcs(canoe: CanoeHandler) -> List[str]:
    """
    Get a list of all active DTCs from the ECU.
    
    Args:
        canoe: CANoe connection handler
        
    Returns:
        List[str]: List of active DTC codes
    """
    # This is a placeholder implementation
    # In real application, would use proper diagnostic messages
    dtcs = []
    if canoe.read_signal("OnOff") == 1:
        dtcs.append("P0123")  # Example DTC
    return dtcs

def clear_dtcs(canoe: CanoeHandler) -> bool:
    """
    Clear all DTCs from the ECU.
    
    Args:
        canoe: CANoe connection handler
        
    Returns:
        bool: True if DTCs were cleared successfully, False otherwise
    """
    try:
        canoe.send_message("EngineState", {
            "OnOff": 0,  # Clear DTCs command
            "EngineSpeed": 0
        })
        return True
    except Exception:
        return False
