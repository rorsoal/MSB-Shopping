# 负责整个项目的配置信息

class Config:
    # 配置数据库和SQLAlchemy
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'test2'
    USERNAME = 'root'
    PASSWORD = '123123'

    DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                            password=PASSWORD,
                                                                                            host=HOSTNAME, port=PORT,
                                                                                db=DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不需要跟踪数据的修改

    # 日志的配置
    LOGGING_LEVEL = 'DEBUG'
    LOGGING_FILE_DIR = 'logs/'
    LOGGING_FILE_MAX_BYTES = 300 * 1024 * 1024
    LOGGING_FILE_BACKUP = 100

    # 限流器采用Redis保存数据，默认是内存，需要安装flask-redis
    RATELIMIT_STORAGE_URL = 'redis://192.168.23.4:6379/0'
    # 限制策略：移动窗口：时间窗口会自动变化
    RATELIMIT_STRATEGY = 'moving-window'

    # redis数据库的连接地址,使用数据库1来存放缓存数据包括短信验证码
    REDIS_URL = "redis://192.168.23.4:6379/1"

# 开发环境下的配置信息
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 打印sql


# 生产环境中的配置信息
class ProductConfig(Config):
    pass
