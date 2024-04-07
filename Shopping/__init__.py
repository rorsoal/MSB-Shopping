from flask import Flask
from settings import map_config

# 负责创建APP
def create_app(config_type):
    app = Flask(__name__)
    # 加载项目的配置
    app.config.from_object(map_config.get(config_type))

    # 初始化限流器
    from comment.utils.limiter import limiter as lmt
    lmt.init_app(app)

    # 加载日志处理的工具
    from comment.utils.logging import create_logger
    create_logger(app)
    # 初始化sqlalchemy
    from comment.models import db
    db.init_app(app)

    # 初始化redis数据库的连接
    from comment.utils.shopping_redis import redis_client
    redis_client.init_app(app)

    # 添加请求钩子
    from comment.utils.requests_wares import jwt_request_authorization
    app.before_request(jwt_request_authorization) # 所有服务器的请求都有当前的请求钩子

    # 加载模块的蓝图
    from Shopping.resources.user import user_bp
    app.register_blueprint(user_bp)

    return app