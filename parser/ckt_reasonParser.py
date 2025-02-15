from parser.parser import Parser

'''
average check time:   0.06320565625240929
final len redundant_clauses:  89
is_sat:  0
correct
Initial SAT: 1, no_dec: 9779.0000
Final SAT: 1, no_dec: 26713.0000
no_dec Reduction: -173.17%
Initial SAT: 1, runtime: 0.2049
Final SAT: 1, runtime: 0.3687
Runtime Reduction: -79.91%
'''

class ckt_reasonParser(Parser):
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
            'avg_check_time': None,
            'redundant_clauses': None,
            'initial_no_dec': None,
            'initial_runtime': None,
            'final_no_dec': None,
            'final_runtime': None,
            'no_dec_reduction': None,
            'runtime_reduction': None,
        }

        for line in self.lines:
            line = line.strip()
            
            # Parse average check time
            if line.startswith('average check time:'):
                self.result['avg_check_time'] = float(line.split(':')[1].strip())
                
            # Parse redundant clauses
            elif line.startswith('final len redundant_clauses:'):
                self.result['redundant_clauses'] = int(line.split(':')[1].strip())
                
            # Parse Initial SAT metrics
            elif line.startswith('Initial SAT:'):
                if 'no_dec:' in line:
                    self.result['initial_no_dec'] = float(line.split('no_dec:')[1].strip())
                elif 'runtime:' in line:
                    self.result['initial_runtime'] = float(line.split('runtime:')[1].strip())
                    
            # Parse Final SAT metrics
            elif line.startswith('Final SAT:'):
                final_sat = int(line.split('SAT:')[1].split(',')[0].strip())
                self.result['predict'] = 'SAT' if final_sat == 1 else 'UNSAT'
                
                if 'no_dec:' in line:
                    self.result['final_no_dec'] = float(line.split('no_dec:')[1].strip())
                elif 'runtime:' in line:
                    self.result['final_runtime'] = float(line.split('runtime:')[1].strip())
                    
            # Parse reduction percentages
            elif 'Reduction:' in line:
                if line.startswith('no_dec'):
                    self.result['no_dec_reduction'] = float(line.split(':')[1].strip().rstrip('%'))
                elif line.startswith('Runtime'):
                    self.result['runtime_reduction'] = float(line.split(':')[1].strip().rstrip('%'))
    
        return self.result
