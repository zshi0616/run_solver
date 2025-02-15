from abc import ABC, abstractmethod

class Parser(ABC):
    def __init__(self, stdout: str):
        """Initialize parser with program stdout
        
        Args:
            stdout (str): Multi-line program output string
        """
        self.stdout = stdout.strip()
        self.lines = self.stdout.split('\n')
        self.result = {}

    @abstractmethod
    def parse(self) -> dict:
        """Parse the stdout and return results as dictionary
        
        Returns:
            dict: Parsed results. The specific format depends on the implementation.
        """
        pass
    

