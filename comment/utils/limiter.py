from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 创建限流器
limiter = Limiter(key_func=get_remote_address)