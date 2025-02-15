from parser.parser import Parser

'''
s SATISFIABLE
Time taken by function: 4.58524 seconds
'''

class EasySATParser(Parser):
    def __init__(self, stdout: str):
        """Initialize parser with program stdout
        
        Args:
            stdout (str): Multi-line program output string
        """
        self.stdout = stdout.strip()
        self.lines = self.stdout.split('\n')
        self.result = {}
        
    def parse(self) -> dict:
        """Parse the stdout and return results as dictionary
        
        Returns:
            dict: Parsed results. The specific format depends on the implementation.
        """
        
        self.result = {
            'predict': None,
            'time': None
        }

        for line in self.lines:
            line = line.strip()
            # Parse solution predict
            if 'SATISFIABLE' in line:
                if 'UNSATISFIABLE' in line:
                    self.result['predict'] = 'UNSAT'
                else:
                    self.result['predict'] = 'SAT'
            
            # Parse time information
            elif 'time' in line.lower():
                try:
                    # Extract number before 's' or 'seconds'
                    time_str = line.split(':')[-1].strip()
                    self.result['time'] = float(time_str.split('s')[0].strip())
                except (ValueError, IndexError):
                    pass

        return self.result
        
        
        
        
    
        
        
        