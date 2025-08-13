"""
Low-level dSPACE automation functions.
"""

class DspaceHandler:
    def __init__(self, model_path: str):
        """Initialize dSPACE connection with the given model path."""
        pass

    def send_signal(self, signal_name: str, value: float):
        """
        Send signal to dSPACE model.
        
        :param signal_name: Name of the signal.
        :param value: Value to set for the signal.
        """
        pass

    def read_signal(self, signal_name: str):
        """
        Read signal from dSPACE model.
        
        :param signal_name: Name of the signal.
        :return: Signal value.
        """
        pass

    def load_model(self, model_path: str):
        """Load the given dSPACE model."""
        pass

    def start_model(self):
        """Start the dSPACE model."""
        pass

    def stop_model(self):
        """Stop the dSPACE model."""
        pass
