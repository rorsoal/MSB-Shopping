# 用户模块下的蓝图，包括用户模块的所有资源

from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

user_bp = Blueprint('users', __name__, url_prefix='/user')  # 创建蓝图
user_api = Api(user_bp)  # 创建蓝图中的资源API

# 在当前用户模块添加请求钩子
# user_bp.before_request()

# 使用我们自定义json格式，替代装饰器的写法
user_api.representation('application/json')(output_json)

# 加载当前模块的资源
from Shopping.resources.user.user_resource import Shopping_User, User_SMS, AuthorizationCodeResource, \
    RegisterUserResource, UserLoginResource

user_api.add_resource(Shopping_User, '/hello', endpoint='user')
user_api.add_resource(User_SMS, '/sms', endpoint='sms')
user_api.add_resource(AuthorizationCodeResource, '/authorization', endpoint='authorization')
user_api.add_resource(RegisterUserResource, '/register', endpoint='register')
user_api.add_resource(UserLoginResource, '/login', endpoint='login')
