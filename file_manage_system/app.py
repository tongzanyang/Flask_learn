# @Version  : 1.0
# @Author   : 故河
# 文件管理系统
'''
功能
1.基本用户登录功能，匿名只可显示出公共文件夹
2.实现基本的文件上传，下载，删除，重命名等基本功能

基本目录结构
1.app程序运行
2.file_manage文件管理软件包
3.file_manage下，settings配置文件
4.files软件包作为文件管理，files下设置upload，download，upload文件夹，login后显示所有文件夹文件到前端。
5.templates和static文件夹存放前端即静态文件。
6.controller业务软件包进行相关的业务操作实现。
'''

from file_manage import app


if __name__ == '__main__':
    app.run(debug=True)