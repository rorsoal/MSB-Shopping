from flask import g

"""
自定义一个装饰器，验证某些请求是否已经登录过了。如果已经登录了继续访问。
本质上就是一个登录拦截
"""


def login_required(func):
    def wrapper(*args, **kwargs):
        if g.user_id is not None:  # 已经登录过了
            return func(*args, **kwargs)
        else:
            return {'message': 'Invalid Token.'}, 401

    return wrapper
