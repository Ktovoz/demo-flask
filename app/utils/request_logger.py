from flask import request, g
from loguru import logger


def get_real_ip():
    """获取真实客户端IP地址"""
    # 检查 X-Forwarded-For 头部
    if request.headers.getlist("X-Forwarded-For"):
        # 第一个IP是真实的客户端IP
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0]
    # 检查其他可能的代理头部
    elif request.headers.get("X-Real-IP"):
        ip = request.headers.get("X-Real-IP")
    elif request.headers.get("X-Forwarded-Host"):
        ip = request.headers.get("X-Forwarded-Host")
    else:
        # 直接获取远程地址
        ip = request.remote_addr
    
    return ip


def log_request_info():
    """记录请求信息"""
    # 获取用户IP
    user_ip = get_real_ip()
    
    # 获取用户代理信息
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # 存储到g对象中供后续使用
    g.user_ip = user_ip
    g.user_agent = user_agent
    
    # 记录请求信息
    logger.info(
        "请求访问 - IP: {ip} | 方法: {method} | 路径: {path} | User-Agent: {user_agent}",
        ip=user_ip,
        method=request.method,
        path=request.path,
        user_agent=user_agent
    )


def log_user_action(action, user=None, extra_data=None):
    """记录用户行为"""
    user_ip = getattr(g, 'user_ip', 'Unknown')
    user_agent = getattr(g, 'user_agent', 'Unknown')
    username = user.username if user else 'Anonymous'
    
    log_data = {
        "操作": action,
        "用户": username,
        "IP": user_ip,
        "User-Agent": user_agent
    }
    
    if extra_data:
        log_data.update(extra_data)
    
    logger.info("用户行为 - {}", log_data)