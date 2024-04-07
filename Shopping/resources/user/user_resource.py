from flask_restful import Resource
from comment.models.user import User
from flask import current_app, request
from comment.utils.aliyun_sms_send import send_sms
import random
import json
from comment.utils.limiter import limiter as lmt
from . import constants
from flask_limiter.util import get_remote_address
from comment.utils.shopping_redis import redis_client
from flask_restful.reqparse import RequestParser
from comment.utils import parser
from comment.models import db
from comment.utils.tokens_pyjwt import generate_tokens, verify_tokens
from comment.utils.decorators import login_required


# 我们定义测试的资源类
class Shopping_User(Resource):
    """
    在get函数上加上登录的拦截
    """
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self): # 测试：当前get函数必须让用户登录之后才能访问
        current_app.logger.info('我的测试日志')
        # 这里的代码可能会用到User模型类
        return {'hello': '测试'}

    def post(self):
        return {'hello': 'post 测试'}

    def put(self):
        return {'hello': 'put 测试'}


class User_SMS(Resource):
    """
    发送验证码的短信，
    """
    error_message = 'Tom many requests.'
    decorators = [
        # 三个参数：参数1：限流的速率,参数2：key_func,参数3：如果超出限制之后的提示信息
        lmt.limit(constants.LIMIT_SMS_CODE_BY_MOBILE,
                  key_func=lambda: request.args['phone'],
                  error_message=error_message),
        lmt.limit(constants.LIMIT_SMS_CODE_BY_IP,
                  key_func=get_remote_address,
                  error_message=error_message)
    ]

    def get(self):
        phone = request.args['phone'].strip()
        code = random.randint(1000, 9999)
        result = send_sms(phone,str(code)) # 返回的是json的字符串
        result = json.loads(result) # 把json编程字典
        # result 往里面添加手机号码
        result['phone'] = phone

        # 短信验证码发送成功之后，还需要把验证码存放到redis数据库中，以便于下次验证，验证码的时效为5分钟
        redis_client.setex('shopping:code:{}'.format(phone), constants.SMS_CODE_EXPIRES, code) # 参数1：key,参数2：时效

        return result


class AuthorizationCodeResource(Resource):

    """
    提交手机号和验证码，开始验证
    """
    def post(self):
        rp = RequestParser()
        rp.add_argument('phone', type=parser.mobile, required=True)
        rp.add_argument('code', type=parser.regex(r'^\d{4}$'), required=True)
        args = rp.parse_args()
        phone = args.phone
        code = args.code

        # 从redis数据库中得到之前保存的验证码
        key = 'shopping:code:{}'.format(phone)
        try:
            real_code = redis_client.get(key) # 从redis中返回的是字节数据
        except ConnectionError as e:
            current_app.logger.error(e)
            return {'message': 'redis db connect error.'},400
        # 开始校验
        if not real_code or real_code.decode() != code:
            return {'message': 'Invalid code.'},400

        return {'phone': phone, 'msg': 'code success.'}


class RegisterUserResource(Resource):

    """
    填写账号信息，完成用户的注册
    """
    def post(self):
        rp = RequestParser()
        rp.add_argument('phone', type=parser.mobile, required=True)
        rp.add_argument('username', required=True)
        rp.add_argument('password', required=True)
        rp.add_argument('email', type=parser.email, required=True)
        args = rp.parse_args()
        username = args.username
        password = args.password
        phone = args.phone
        email = args.email

        # 验证用户名是否唯一 :先从mysql数据库中根据当前用户名查询
        u = User.query.filter(User.username == username).first()
        if u:  # 用户名已经存在
            current_app.logger.info('{}:用户名已经存在，请换一个'.format(username))
            return {'msg': 'The username already exists.'}, 400

        # 把用户信息保存到数据库中
        u = User(username=username ,pwd=password, email=email,status=0)
        db.session.add(u)
        db.session.commit()
        return {'msg': 'ok'}


class UserLoginResource(Resource):
    """
    登录
    """
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username,password]):
            return {'message': '数据不完整'}, 402
        user = User.query.filter(User.username == username).first()
        if user:
            if user.check_password(password):
                # 必须把登录成功之后的用户 ID得到token，token返回给前端
                token = generate_tokens(user.id)
                current_app.logger.info(verify_tokens(token))
                return {'msg': 'Login Success.', 'token': token}
        return {'message': '用户名或者密码错误.'}, 400