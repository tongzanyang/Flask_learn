# @Version  : 1.0
# @Author   : 故河
import os.path
from flask import request
from flask_restful import Resource
from file_manage.setting import PUBLIC_FILE
from file_manage import api

# 写一个可调用的文件上传API
'''
思路分析
1.首先获取上传的文件,判断是否存在
2.存在则获取filename通过os模块保存文件到指定的公共目录。
需判断文件名是否为空，是否存在files字段，是否文件名重复（避免重复上传）
'''

# 指定文件存放目录
public_file = PUBLIC_FILE

class FILEs_UPLOAD(Resource):
    def post(self):
        if 'files' not in request.files:
            return {
                'success': False,
                'message': '未选择文件'
            }, 400

        files = request.files['files']

        filename = files.filename

        # 检查文件名是否为空
        if files.filename == '':
            return {
                'success': False,
                'message': '未选择文件'
            }, 400

        # 保存文件到目录
        file_path = os.path.join(PUBLIC_FILE, filename)

        # 避免文件名冲突
        if os.path.exists(file_path):
            return {
                'success': False,
                'message': '文件已存在'
            }, 400

        files.save(file_path)

        return {
            'success': True,
            'message': '文件上传成功',
            'filename': filename
        }, 200


api.add_resource(FILEs_UPLOAD, "/api/v1/upload")
