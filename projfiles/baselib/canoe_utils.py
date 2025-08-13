"""
Low-level CANoe connection and control functions.
"""
from typing import Dict, Any, Optional, Union, List
import time
import win32com.client
from pathlib import Path

class CanoeHandler:
    def __init__(self, config_path: str):
        """Initialize CANoe connection with provided configuration file path.
        
        Args:
            config_path (str): Path to the CANoe configuration file
        """
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            raise FileNotFoundError(f"CANoe configuration file not found: {config_path}")
        
        self.connected = False
        self.app = None
        self.measurement = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to CANoe using COM interface.
        
        Raises:
            RuntimeError: If CANoe application can't be started
            FileNotFoundError: If configuration file doesn't exist
        """
        try:
            # Get CANoe dispatch object
            self.app = win32com.client.Dispatch("CANoe.Application")
            # Load configuration
            self.app.Open(str(self.config_path))
            # Get measurement interface
            self.measurement = self.app.Measurement
            self.connected = True
        except Exception as e:
            raise RuntimeError(f"Failed to connect to CANoe: {str(e)}")

    def start_measurement(self) -> None:
        """Start CANoe measurement."""
        if not self.connected:
            raise ConnectionError("Not connected to CANoe")
        try:
            self.measurement.Start()
        except Exception as e:
            raise RuntimeError(f"Failed to start measurement: {str(e)}")

    def stop_measurement(self) -> None:
        """Stop CANoe measurement."""
        if not self.connected:
            raise ConnectionError("Not connected to CANoe")
        try:
            self.measurement.Stop()
        except Exception as e:
            raise RuntimeError(f"Failed to stop measurement: {str(e)}")

    def read_signal(self, signal_name: str) -> Union[float, int, bool, str]:
        """
        Read a signal value from CANoe.
        
        Args:
            signal_name (str): Name of the signal to read
            
        Returns:
            Union[float, int, bool, str]: The current value of the signal
            
        Raises:
            ValueError: If signal name is invalid
            ConnectionError: If not connected to CANoe
        """
        if not self.connected:
            raise ConnectionError("Not connected to CANoe")
            
        try:
            bus_signal = self.app.Bus.GetSignal(signal_name)
            return bus_signal.Value
        except Exception as e:
            raise ValueError(f"Failed to read signal {signal_name}: {str(e)}")

    def write_signal(self, signal_name: str, value: Union[float, int, bool, str]) -> None:
        """
        Write a value to a CANoe signal.
        
        Args:
            signal_name (str): Name of the signal to write
            value: Value to write to the signal
            
        Raises:
            ValueError: If signal name is invalid or value type is incorrect
            ConnectionError: If not connected to CANoe
        """
        if not self.connected:
            raise ConnectionError("Not connected to CANoe")
            
        try:
            bus_signal = self.app.Bus.GetSignal(signal_name)
            bus_signal.Value = value
        except Exception as e:
            raise ValueError(f"Failed to write signal {signal_name}: {str(e)}")
            
    def get_environment_variable(self, var_name: str) -> Any:
        """
        Get the value of a CANoe environment variable.
        
        Args:
            var_name (str): Name of the environment variable
            
        Returns:
            Any: Value of the environment variable
            
        Raises:
            ValueError: If variable name is invalid
            ConnectionError: If not connected to CANoe
        """
        if not self.connected:
            raise ConnectionError("Not connected to CANoe")
            
        try:
            env_var = self.app.Environment.GetVariable(var_name)
            return env_var.Value
        except Exception as e:
            raise ValueError(f"Failed to read environment variable {var_name}: {str(e)}")
            
    def set_environment_variable(self, var_name: str, value: Any) -> None:
        """
        Set the value of a CANoe environment variable.
        
        Args:
            var_name (str): Name of the environment variable
            value: Value to set
            
        Raises:
            ValueError: If variable name is invalid or value type is incorrect
            ConnectionError: If not connected to CANoe
        """
        if not self.connected:
            raise ConnectionError("Not connected to CANoe")
            
        try:
            env_var = self.app.Environment.GetVariable(var_name)
            env_var.Value = value
        except Exception as e:
            raise ValueError(f"Failed to write environment variable {var_name}: {str(e)}")

    def close(self) -> None:
        """Close the connection to CANoe and quit the application."""
        if self.connected:
            try:
                self.app.Quit()
            except:
                pass
            finally:
                self.app = None
                self.measurement = None
                self.connected = False
