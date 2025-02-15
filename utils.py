import sys
import csv
import os 

from pathlib import Path
from parser.EasySATParser import EasySATParser
from parser.kissatParser import kissatParser
from parser.ckt_reasonParser import ckt_reasonParser

class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, 'w', encoding='utf-8')
    
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()
        
    def flush(self):
        self.terminal.flush()
        self.log.flush()
        
def get_solver(solver):
    solver_run_cmd = '{}/build/kissat'.format(solver)
    parser_class = kissatParser
    if not os.path.exists(solver_run_cmd):
        raise FileNotFoundError(f"Solver executable not found: {solver_run_cmd}")
    # # Configure solver and parser
    # if solver == 'EasySAT':
    #     from parser.EasySATParser import EasySATParser
    #     solver_run_cmd = './../EasySAT/EasySAT'
    #     parser_class = EasySATParser
    # elif solver == 'kissat':
    #     from parser.kissatParser import kissatParser
    #     solver_run_cmd = './kissat/build/kissat'
    #     parser_class = kissatParser
    # elif solver == 'ckt_reason':
    #     from parser.ckt_reasonParser import ckt_reasonParser
    #     solver_run_cmd = 'python ../ckt_reason/src/main.py --cases'
    #     parser_class = ckt_reasonParser
    # elif solver == 'cadical':
    #     from parser.cadicalParser import cadicalParser
    #     solver_run_cmd = './../cadical/build/cadical'
    #     parser_class = cadicalParser
    # elif solver == 'CaiSAT_cadical':
    #     from parser.cadicalParser import cadicalParser
    #     solver_run_cmd = './../CaiSAT_cadical/build/cadical'
    #     parser_class = cadicalParser
    # else:
    #     raise NotImplementedError(f'Solver {solver} not implemented')
    
    return solver_run_cmd, parser_class
        
def save_result(results, result_dir):
    """Save test results to a CSV file
    
    Args:
        results (dict): Dictionary containing test results
        result_dir (str/Path): Directory to save the results
    """
    result_file = Path(result_dir) / "results.csv"
    
    # Find first non-None result to get headers
    headers = None
    for result in results.values():
        if result and isinstance(result, dict) and result['predict'] != 'error' and result['predict'] != None:
            # Verify required fields exist
            required_fields = {'test_case', 'predict', 'target'}
            if not required_fields.issubset(result.keys()):
                print(f"❌ Missing required fields. Found: {result.keys()}")
                print(f"   Required: {required_fields}")
                return
                
            # Arrange headers in required order
            headers = ['test_case']  # First position
            
            # Add other fields (excluding test_case, predict, target)
            other_fields = [f for f in result.keys() 
                          if f not in {'test_case', 'predict', 'target'}]
            headers.extend(other_fields)
            
            # Add predict and target at the end
            headers.extend(['predict', 'target'])  # Last positions
            break
    
    if not headers:
        print("❌ No valid results found to save")
        return
    
    print(f"\n💾 Saving results to: {result_file}")
    
    try:
        with open(result_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            
            # Write headers
            writer.writeheader()
            
            # Write results
            for test_case, result in results.items():
                if result:  # Skip None results
                    writer.writerow(result)
        
        print(f"✅ Results saved successfully")
        print(f"   • Total entries: {sum(1 for r in results.values() if r)}")
        print(f"   • Fields: {', '.join(headers)}")
        
    except Exception as e:
        print(f"❌ Error saving results: {e}")
        
        
