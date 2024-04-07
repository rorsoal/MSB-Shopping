"""
定义请求钩子： 在请求进来之前得到request携带的token，并且验证token
"""
from flask import g, request, current_app
from comment.utils.tokens_pyjwt import verify_tokens


def jwt_request_authorization():
    """
    自定义一个请求钩子函数，验证token，并且把验证成功之后的用户ID保存到全局变量g中
    :return:
    """
    g.user_id = None # 定义一个变量user_id
    try:
        token = request.headers.get('token')
    except Exception as ex:
        current_app.logger.info('请求头中没有token')
        return
    result = verify_tokens(token)
    if 'id' in result:  # 如果验证成功，那么字典中一定有用户ID
        g.user_id = result['id']