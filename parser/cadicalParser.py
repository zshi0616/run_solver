from parser.parser import Parser

class cadicalParser(Parser):
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
            dict: Parsed results with all metrics as individual fields
        """
        
        self.result = {
            'predict': None,
            'time': None,
            'conflicts': None,
            'decisions': None
        }

        for line in self.lines:
            line = line.strip()
            
            # Parse solution predict
            if 'SATISFIABLE' in line:
                if 'UNSATISFIABLE' in line:
                    self.result['predict'] = 'UNSAT'
                else:
                    self.result['predict'] = 'SAT'
            elif 'total real time' in line.lower():
                try:
                    # Extract number before 's' or 'seconds'
                    time_str = line.split(':')[-1].strip()
                    self.result['time'] = float(time_str.split('s')[0].strip())
                except (ValueError, IndexError):
                    pass
            # Parse metrics from log lines
            else:
                # 检查行中是否包含任何预定义的指标名称
                for metric_name in self.result.keys():
                    if metric_name != 'predict' and metric_name != 'time' and f"{metric_name}:" in line:
                        try:
                            parts = line.split()
                            # 找到指标名称后的第一个数字
                            for part in parts:
                                try:
                                    value = float(part)
                                    self.result[metric_name] = value
                                    break
                                except ValueError:
                                    continue
                        except (ValueError, IndexError):
                            continue

        return self.result
