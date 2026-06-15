from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseConnector(ABC):
    @abstractmethod
    async def execute(self, config: Dict[str, Any], params: Dict[str, Any], context_data: Dict[str, Any]) -> Any:
        """
        Execute the connector logic.
        :param config: The configuration dictionary from the Integration database model.
        :param params: The step-specific parameters.
        :param context_data: Context data passed from previous steps.
        :return: Execution result
        """
        pass
