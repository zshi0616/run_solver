import os
import subprocess
import time
import sys
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from utils import get_solver

def setup_logging(result_dir):
    """Setup logging configuration"""
    log_file = Path(result_dir) / "log.txt"
    
    # 创建格式化器
    formatter = logging.Formatter('%(message)s')
    
    # 创建并配置文件处理器
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # 创建并配置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 获取根日志记录器并配置
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def run_single_test(test_case_path, test_args, solver_run_cmd, parser_class, timeout, result_dir):
    """Run a single test case and parse its output"""
    test_case = test_case_path.split('/')[-1].split('.')[0]
    logging.info(f"🔄 Running test case: {test_case}")
    start_time = time.time()
    
    try:
        cmd = f"{solver_run_cmd} {test_args} {test_case_path}"
        # print(cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            # Saved info
            parser = parser_class(stdout.decode())
            
            pos = stdout.decode().find('---- [ result ] ------')
            if pos != -1:
                save_info = stdout[pos:]
                single_log_path = os.path.join(result_dir, 'single_logs', f'{test_case}.log')
                single_log_file = open(single_log_path, 'w')
                save_info = str(save_info).replace('\\n', '\n')
                single_log_file.write(save_info)
                single_log_file.close()
            
            result = parser.parse()
            result['test_case'] = test_case
            logging.info(f"✅ {test_case} completed in {round(time.time() - start_time, 2)}s")
            return result 
        except subprocess.TimeoutExpired:
            process.kill()
            logging.warning(f"⏰ Test case {test_case} timed out after {timeout} seconds")
            result = {
                'test_case': test_case,
                'predict': 'error', 
                'time': timeout
            }
            return result
    except Exception as e:
        logging.error(f"❌ Error running test case {test_case}: {e}")
        raise e

def test(test_case_paths, test_args, solver, thread_num, timeout, test_cases_dict, result_dir):
    """Run test cases in parallel and collect results"""
    # 设置日志
    logger = setup_logging(result_dir)
    
    try:
        logging.info("\n" + "="*60)
        logging.info(f"🚀 Test Session Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info("="*60)
        
        logging.info(f"\n📋 Test Configuration:")
        logging.info(f"   • Solver: {solver}")
        logging.info(f"   • Thread Count: {thread_num}")
        logging.info(f"   • Timeout: {timeout}s")
        logging.info(f"   • Total Test Cases: {len(test_case_paths)}")
        
        # Configure solver and parser
        solver_run_cmd, parser_class = get_solver(solver)
        if not os.path.exists(solver_run_cmd):
            raise FileNotFoundError(f"Solver executable not found: {solver_run_cmd}")
        
        if solver == 'ckt_reason':
            test_case_paths = [test_case_path.split('/')[-1].split('.')[0] for test_case_path in test_case_paths]
            
        results = {}
        start_time = time.time()
        
        logging.info("\n⚡ Starting Test Execution...\n")
        logging.info("-"*60)
        
        # Create thread pool and run tests in parallel
        with ThreadPoolExecutor(max_workers=thread_num) as executor:
            future_to_test = {
                executor.submit(run_single_test, test_case_path, test_args, solver_run_cmd, parser_class, timeout, result_dir): test_case_path
                for test_case_path in test_case_paths
            }
            print()
            
            completed = 0
            for future in as_completed(future_to_test):
                completed += 1
                test_case = future_to_test[future].split('/')[-1].split('.')[0]
                try:
                    result = future.result()
                    result['target'] = 'SAT' if test_case in test_cases_dict['SAT'] else 'UNSAT'
                    results[test_case] = result
                    progress = (completed / len(test_case_paths)) * 100
                    logging.info(f"📊 Progress: {progress:.1f}% ({completed}/{len(test_case_paths)})")
                except Exception as e:
                    results[test_case] = {
                        'test_case': test_case,
                        'predict': 'error',
                        'result': None,
                        'error': str(e)
                    }
        
        total_time = round(time.time() - start_time, 2)
        
        all_time = 0
        for result in results:
            all_time += results[result]['time']
        
        logging.info("\n" + "="*60)
        logging.info(f"🏁 Test Session Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"\n📊 Summary:")
        logging.info(f"   • Runtime: {total_time}s")
        logging.info(f"   • Total solve time: {all_time}s")
        logging.info(f"   • Total Cases: {len(results)}")
        
        success_count = sum(1 for r in results.values() if r and r.get('predict') != 'error')
        # correct_count = sum(1 for r in results.values() if r and r.get('predict') != 'error' and r.get('predict') == r.get('target'))
        # incorrect_count = sum(1 for r in results.values() if r and r.get('predict') != 'error' and r.get('predict') != r.get('target'))
        logging.info(f"   • ✅ Successful: {success_count}")
        # logging.info(f"       • ✅ Correct: {correct_count}")
        # logging.info(f"       • ❌ Incorrect: {incorrect_count}")
        
        error_count = sum(1 for r in results.values() if not r or r.get('predict') == 'error')
        logging.info(f"   • ❌ Failed: {error_count}")
        logging.info("="*60 + "\n")
        
        return results
        
    finally:
        # 清理日志处理器
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

def test_init(solver):
    """Initialize test environment by creating result directory"""
    # Create result directory with solver name and timestamp
    result_dir = Path('result') / f'{solver}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
    
    # Create directories
    result_dir.mkdir(parents=True, exist_ok=True)
    single_logs_dir = result_dir / 'single_logs'
    single_logs_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Created result directory: {result_dir}")
    print(f"📁 Created single_logs directory: {single_logs_dir}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return result_dir
