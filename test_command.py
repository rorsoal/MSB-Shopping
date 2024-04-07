#  当前的命令调用Flask要和Web主程序分离

from flask_script import Manager
from Shopping import create_app
from flask_sqlalchemy import SQLAlchemy
app = create_app('develop')
db = SQLAlchemy(app)
manager = Manager(app)

class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    uname = db.Column(db.String(50),nullable=False)
    pwd = db.Column(db.String(50),nullable=False)

# db.create_all()
@manager.command
def hello():
    print("你的命令执行成功")


# 通过命令直接在数据库中创建一个用户
@manager.option("-u","--username",dest="x_uname")
@manager.option("-p","--password",dest="x_pwd")
def create_user(x_uname,x_pwd):
    user = User(uname=x_uname,pwd=x_pwd)
    db.session.add(user)
    db.session.commit()
    print("执行命令添加用户成功！")

if __name__ == '__main__':
    manager.run()
