"""
Low-level CANoe connection and control functions.
"""

class CanoeHandler:
    def __init__(self, config_path: str):
        """Initialize CANoe connection with provided configuration file path."""
        pass

    def start_measurement(self):
        """Start CANoe measurement."""
        pass

    def stop_measurement(self):
        """Stop CANoe measurement."""
        pass

    def read_signal(self, signal_name: str):
        """
        Read a signal value from CANoe.
        
        :param signal_name: Name of the signal to read.
        :return: Signal value.
        """
        pass

    def send_message(self, message_name: str, data: dict):
        """
        Send a CAN message with given data.
        
        :param message_name: Name of the CAN message.
        :param data: Dictionary of signal-value pairs to send.
        """
        pass
