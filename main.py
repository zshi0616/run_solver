import os
import json
import glob
import argparse

from test import test_init, test
from utils import save_result

def parse_args():
    parser = argparse.ArgumentParser(description='Test program argument parser')
    
    # Add solver parameter
    parser.add_argument('--solver', type=str, required=True,
                      help='name of the solver')
    
    # Add testcases parameter, supports single case or multiple cases
    parser.add_argument('--testcases', type=str, required=True,
                      help='testcase can be single case(test1), case list[test1, test2, test3], "SAT", "UNSAT" or "all"')
    
    # Add thread number parameter
    parser.add_argument('--thread_num', type=int, default=8,
                      help='number of threads (default: 8)')
    
    # Add testcases file format
    parser.add_argument('--format', type=str, required=True, default='cnf',
                      help='testcase format can be "cnf", "aag"')
    
    # Add timeout parameter
    parser.add_argument('--timeout', type=int, default=60,
                      help='timeout for each test case (default: 60 seconds)')
    
    # Add args parameter
    parser.add_argument('--args', type=str, default='',
                      help='args for solver')
    
    # Add quiet option 
    parser.add_argument('--quiet', action='store_true', default=False, help='quiet mode')
    
    args = parser.parse_args()
    
    # # Initialize list to store test case paths
    # test_case_paths = []
    # base_path = os.path.join('testcases', args.format)
    # json_path = os.path.join('testcases', 'testcases.json')
    # with open(json_path, 'r') as f:
    #     test_cases_dict = json.load(f)
    
    # # Process testcases parameter
    # if args.testcases.lower() == 'all':
    #     # Get all cases from both SAT and UNSAT directories
    #     sat_path = os.path.join(base_path, 'SAT', f'*.{args.format}')
    #     unsat_path = os.path.join(base_path, 'UNSAT', f'*.{args.format}')
    #     test_case_paths.extend(glob.glob(sat_path))
    #     test_case_paths.extend(glob.glob(unsat_path))
    
    # elif args.testcases.upper() in ['SAT', 'UNSAT']:
    #     # Get all cases from specified directory
    #     path = os.path.join(base_path, args.testcases.upper(), f'*.{args.format}')
    #     test_case_paths.extend(glob.glob(path))
    
    # else:
    #     if args.testcases.startswith('[') and args.testcases.endswith(']'):
    #         cases = [x.strip() for x in args.testcases[1:-1].split(',')]
    #     else:
    #         cases = [args.testcases]
        
    #     # Find each case in SAT or UNSAT directories
    #     for case in cases:
    #         case_name = case.replace(f'.{args.format}', '')
    #         # Check in SAT cases
    #         if case_name in test_cases_dict['SAT']:
    #             path = os.path.join(base_path, 'SAT', f'{case_name}.{args.format}')
    #             test_case_paths.append(path)
    #         # Check in UNSAT cases
    #         else:
    #             path = os.path.join(base_path, 'UNSAT', f'{case_name}.{args.format}')
    #             test_case_paths.append(path)
    
    # Testcases 
    test_case_paths = glob.glob(os.path.join(args.testcases, '*.{}'.format(args.format)))
    test_cases_dict = {}
    test_cases_dict['SAT'] = []
    for test_case in test_case_paths:
        test_name = os.path.basename(test_case).split('.')[0]
        test_cases_dict['SAT'].append(test_name)
    
    # Store the paths in args
    args.test_case_paths = test_case_paths
    return args, test_cases_dict

if __name__ == '__main__':
    args, test_cases_dict = parse_args()
    
    result_dir = test_init(args.solver)  
    results = test(args.test_case_paths, args.args, args.solver, args.thread_num, args.timeout, test_cases_dict, result_dir, args.quiet)
    save_result(results, result_dir)
