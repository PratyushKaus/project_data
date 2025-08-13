"""
Low-level dSPACE automation functions.
"""
from typing import Dict, Any, Optional, Union
import time
from pathlib import Path

try:
    import pythoncom
    import win32com.client
except ImportError:
    raise ImportError("pywin32 is required for dSPACE automation. Install with: pip install pywin32")

class DspaceHandler:
    def __init__(self, model_path: str):
        """Initialize dSPACE connection with the given model file.
        
        Args:
            model_path (str): Path to the dSPACE model file (.sdf)
        """
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"dSPACE model file not found: {model_path}")
            
        self.connected = False
        self.model_running = False
        self.app = None
        self.variables = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to dSPACE system using Python COM interface.
        
        Raises:
            RuntimeError: If connection fails
        """
        try:
            # Initialize COM for this thread
            pythoncom.CoInitialize()
            
            # Connect to dSPACE Control Desk
            self.app = win32com.client.Dispatch("dSPACE.Application")
            
            # Load the model
            self.app.Load(str(self.model_path))
            
            # Get variable interface
            self.variables = self.app.Variables
            self.connected = True
            
        except Exception as e:
            raise RuntimeError(f"Failed to connect to dSPACE: {str(e)}")

    def start_model(self) -> None:
        """Start the dSPACE model.
        
        Raises:
            ConnectionError: If not connected to dSPACE
            RuntimeError: If model fails to start
        """
        if not self.connected:
            raise ConnectionError("Not connected to dSPACE")
            
        try:
            self.app.StartModel()
            self.model_running = True
        except Exception as e:
            raise RuntimeError(f"Failed to start model: {str(e)}")

    def stop_model(self) -> None:
        """Stop the dSPACE model.
        
        Raises:
            ConnectionError: If not connected to dSPACE
            RuntimeError: If model fails to stop
        """
        if not self.connected:
            raise ConnectionError("Not connected to dSPACE")
            
        try:
            self.app.StopModel()
            self.model_running = False
        except Exception as e:
            raise RuntimeError(f"Failed to stop model: {str(e)}")

    def send_signal(self, signal_name: str, value: Union[float, int, bool]) -> None:
        """
        Send signal to dSPACE model.
        
        Args:
            signal_name (str): Name of the signal
            value (Union[float, int, bool]): Value to set for the signal
            
        Raises:
            ConnectionError: If not connected to dSPACE
            ValueError: If signal name is invalid
            RuntimeError: If model is not running
        """
        if not self.connected:
            raise ConnectionError("Not connected to dSPACE")
        if not self.model_running:
            raise RuntimeError("Model is not running")
            
        try:
            variable = self.variables.Item(signal_name)
            variable.Value = value
        except Exception as e:
            raise ValueError(f"Failed to write signal {signal_name}: {str(e)}")

    def read_signal(self, signal_name: str) -> Union[float, int, bool]:
        """
        Read signal from dSPACE model.
        
        Args:
            signal_name (str): Name of the signal to read
            
        Returns:
            Union[float, int, bool]: Current value of the signal
            
        Raises:
            ConnectionError: If not connected to dSPACE
            ValueError: If signal name is invalid
            RuntimeError: If model is not running
        """
        if not self.connected:
            raise ConnectionError("Not connected to dSPACE")
        if not self.model_running:
            raise RuntimeError("Model is not running")
            
        try:
            variable = self.variables.Item(signal_name)
            return variable.Value
        except Exception as e:
            raise ValueError(f"Failed to read signal {signal_name}: {str(e)}")
            
    def get_variable_info(self, var_name: str) -> Dict[str, Any]:
        """
        Get information about a model variable.
        
        Args:
            var_name (str): Name of the variable
            
        Returns:
            Dict[str, Any]: Dictionary containing variable information
            
        Raises:
            ConnectionError: If not connected to dSPACE
            ValueError: If variable name is invalid
        """
        if not self.connected:
            raise ConnectionError("Not connected to dSPACE")
            
        try:
            variable = self.variables.Item(var_name)
            return {
                'name': variable.Name,
                'type': variable.Type,
                'unit': variable.Unit,
                'description': variable.Description,
                'min_value': variable.MinValue,
                'max_value': variable.MaxValue
            }
        except Exception as e:
            raise ValueError(f"Failed to get variable info for {var_name}: {str(e)}")

    def close(self) -> None:
        """Close the connection to dSPACE and clean up COM objects."""
        if self.connected:
            try:
                if self.model_running:
                    self.stop_model()
                self.app.Quit()
            except:
                pass
            finally:
                self.app = None
                self.variables = None
                self.connected = False
                pythoncom.CoUninitialize()
