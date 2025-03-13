# @Version  : 1.0
# @Author   : 故河
import pymysql
pymysql.install_as_MySQLdb()

#调试模式是否开启
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
#session必须要设置key
SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#mysql数据库连接信息,这里改为自己的账号
SQLALCHEMY_DATABASE_URI = "mysql://root:t04241003+@localhost:3306/my_blog_db"
