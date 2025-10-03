import re
from datetime import datetime
from colorama import Fore, Style, init

# 初始化colorama
init(autoreset=True)

def parse_log_line(line):
    """解析单行日志"""
    # 匹配时间戳、日志级别、模块和消息
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \| (\w+) *\| ([^:]+:\d+) - (.*)'
    match = re.match(pattern, line)
    
    if match:
        timestamp, level, module, message = match.groups()
        return {
            'timestamp': timestamp,
            'level': level,
            'module': module,
            'message': message
        }
    else:
        # 如果不匹配常规格式，返回原始行
        return {'raw': line}

def colorize_level(level):
    """根据日志级别返回带颜色的字符串"""
    colors = {
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'DEBUG': Fore.CYAN,
        'CRITICAL': Fore.MAGENTA,
        'SUCCESS': Fore.GREEN
    }
    return colors.get(level, '') + level + Style.RESET_ALL

def beautify_logs(input_text):
    """美化日志文本"""
    lines = input_text.strip().split('\n')
    formatted_lines = []
    
    for line in lines:
        # 移除ANSI转义序列
        line = re.sub(r'\x1b\[[0-9;]*m', '', line)
        parsed = parse_log_line(line)
        
        if 'raw' in parsed:
            formatted_lines.append(parsed['raw'])
        else:
            # 格式化标准日志行
            timestamp = parsed['timestamp']
            level = colorize_level(parsed['level'])
            module = Fore.BLUE + parsed['module'] + Style.RESET_ALL
            message = parsed['message']
            
            formatted_line = f"[{Fore.CYAN}{timestamp}{Style.RESET_ALL}] {level:8} | {module:<30} | {message}"
            formatted_lines.append(formatted_line)
    
    return '\n'.join(formatted_lines)

if __name__ == "__main__":
    # 读取日志文件
    with open('instance/logs/app.log', 'r', encoding='utf-8') as f:
        log_content = f.read()
    
    # 美化日志
    beautified = beautify_logs(log_content)
    
    # 打印美化后的日志
    print(beautified)