from itsdangerous import TimedJSONWebSignatureSerializer
from comment.utils import const
from flask import current_app
from comment.models.user import User


def generate_tokens(uid):
    """
    根据已经登录之后的用户ID，生成token
    :param uid: 用户ID
    :return:
    """
    # 参数1: 秘钥，参数2：token有效时间
    s = TimedJSONWebSignatureSerializer(secret_key=const.SECRET_KEY,expires_in=const.JWT_EXPIRY_SECOND)
    # 生成token
    return s.dumps({'id': uid}).decode()


def verify_tokens(token_str):
    """
    验证token，并且验证成功之后，返回用户ID
    :param token_str:
    :return:
    """
    s = TimedJSONWebSignatureSerializer(secret_key=const.SECRET_KEY)
    try:
        data = s.loads(token_str) # 本质上就是一个解密的过程
    except Exception as e:
        current_app.logger.info(e)
        return {'message': 'token 验证失败'}
    # 如果token验证成功，还需要看看当前用户状态是否正常
    user = User.query.filter(User.id == data['id']).first()
    if user and user.status != 0:
        return {'message': '数据库中的用户状态过期'}
    return {'id': user.id}