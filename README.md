# SAT Solver Test Framework

一个用于测试 SAT 求解器的自动化测试框架。支持并行测试执行、超时控制和结果分析。

## 功能特点

- 并行测试执行
- 超时控制
- 自动结果收集和分析
- 详细的测试报告生成

## 使用方法

### 基本命令

```bash
python main.py --solver <solver_dir> --testcases <test_dir> --thread_num <threads> --timeout <timeout> --args=<args>
```

### 参数说明

- `--solver`: 求解器目录 (必需)
  - 需要将求解器保存到该目录下
  - 比如 --solver kissat-4.0.0 将会在./kissat-4.0.0/build/kissat寻找求解器

- `--testcases`: 测试用例选择 (必需)
  - 需要指定保存CNF格式测试用例的目录

- `--thread_num`: 并行执行的线程数 (可选)
  - 默认值: 8

- `--timeout`: 超时时间 (单位: 秒, 可选)
  - 默认值: 60
  - 如果不想限时，设置一个极大的timeout即可（不建议）

- `--args`: 求解器参数 (可选)
  - 默认值: 空
  - 例如：`--args "--quiet"`

### 示例

```bash
python main.py --solver EasySAT --testcases all --format cnf --thread_num 4
```

```bash
python main.py --solver cadical --testcases SAT --format cnf --thread_num 4 --args="--default"
```

## 输出说明

### 测试结果

测试结果将保存在 `result/<solver>_<timestamp>/` 目录下：
- `log.txt`: 详细的测试执行日志
- `results.csv`: 测试结果汇总，包含以下字段：
  - `test_case`: 测试用例名称
  - `predict`: 求解器输出结果
  - `target`: 预期结果
  - `other`: 其他字段

对于每一个测试用例的log，会保存在 `result/<solver>_<timestamp>/single_logs/` 目录下。

## Parser说明

Parser 是一个抽象基类，用于解析不同求解器的输出。每个具体的求解器都需要实现自己的 Parser 类

### 基类 Parser
```python
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
```
对于不同的求解器，需要对应实现自己的Parser类，并放在`parser/`目录下。

这个对应的Parser类必须继承自基类Parser，并且必须实现parse方法。parse方法的返回值是一个字典，字典的键值对需要根据具体需求来确定，必须要返回`predict`键值对。

写法可参考`parser/EasySATParser.py`和`parser/kissatParser.py`。
## 目录结构

```
test/
├── parser/
│   ├── parser.py
│   └── EasySATParser.py
│   └── kissatParser.py
│   └── ckt_reasonParser.py
├── result/
├── utils.py
├── test.py
└── main.py
```