import logging
import logging.handlers
from flask import request
import os


class RequestShoppingFormatter(logging.Formatter):
    """
    自定义的日志输出格式
    """

    def format(self, record):
        record.url = request.url  # 需要在日志中记录请求地址
        record.remote_addr = request.remote_addr  # 需要在日志中记录客户端的地址
        return super().format(record)


# 创建一个个性化的logger对象
def create_logger(app):
    """
    设置日志配置
    :param app: Flask中的app对象
    :return:
    """
    logging_file_dir = app.config['LOGGING_FILE_DIR']  # 日志文件所在的目录
    logging_file_max_bytes = app.config['LOGGING_FILE_MAX_BYTES']  # 日志文件最大的大小
    logging_file_backup = app.config['LOGGING_FILE_BACKUP']  # 保留备份的日志文件个数
    logging_level = app.config['LOGGING_LEVEL']  # 默认的日志级别

    # 设置日志的输出格式(针对文件)
    request_formatter = RequestShoppingFormatter(
        '[%(asctime)s] %(remote_addr)s  请求 %(url)s \t %(levelname)s 在 %(module)s %(lineno)d : %(message)s')


    # 检查如果目录不存在，则创建目录
    if os.path.isdir(logging_file_dir):
        pass
    else:
        os.mkdir(logging_file_dir)  # 如果目录不存在，创建

    # 自定义一个目录和日志文件
    flask_file_handler = logging.handlers.RotatingFileHandler(filename=os.path.join(logging_file_dir, 'shopping.log'),
                                         maxBytes=logging_file_max_bytes,
                                         backupCount=logging_file_backup)

    # 给当前的handler设置格式
    flask_file_handler.setFormatter(request_formatter)
    # 得到一个logger对象
    flask_logger = logging.getLogger('Shopping')
    flask_logger.addHandler(flask_file_handler)
    flask_logger.setLevel(logging_level)

    # 整个项目需要两个handler：文件，控制台
    flask_console_handler = logging.StreamHandler()
    flask_console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(module)s %(lineno)d : %('
                                                         'message)s'))

    # 当项目运行环境是debug，才用控制台输出
    if app.debug:
        flask_logger.addHandler(flask_console_handler)
