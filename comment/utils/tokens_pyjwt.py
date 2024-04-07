import jwt
from jwt import PyJWTError

from comment.utils import const
from flask import current_app
from comment.models.user import User
from datetime import datetime, timedelta


def generate_tokens(uid):
    """
    根据已经登录之后的用户ID，生成token
    :param uid: 用户ID
    :return:
    """
    payload = {
        'id': uid,
        # exp代表token有效时间，而且必须是标准时间
        'exp': datetime.utcnow() + timedelta(seconds=const.JWT_EXPIRY_SECOND)
    }
    # 参数1: payload是一个字典包括加密的用户ID和有效时间，参数2：秘钥，参数3： 算法
    s = jwt.encode(payload=payload,key=const.SECRET_KEY, algorithm='HS256')
    # 生成token
    return s


def verify_tokens(token_str):
    """
    验证token，并且验证成功之后，返回用户ID
    :param token_str:
    :return:
    """
    try:
        # 本质上就是一个解密的过程
        data = jwt.decode(token_str, key=const.SECRET_KEY, algorithms='HS256')
        current_app.logger.info(data)
    except PyJWTError as e:
        current_app.logger.info(e)
        return {'message': 'token 验证失败'}
    # 如果token验证成功，还需要看看当前用户状态是否正常
    user = User.query.filter(User.id == data['id']).first()
    if user and user.status != 0:
        return {'message': '数据库中的用户状态过期'}
    return {'id': user.id}