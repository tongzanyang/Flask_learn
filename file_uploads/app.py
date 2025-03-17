from flask import Flask, render_template, request, send_from_directory
from flask_restful import Api, Resource
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制文件大小为16MB

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

api = Api(app)

@app.route('/')
def index():
    '''
    系统界面
    :return:前端
    '''
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    '''
    上传文件
    :return:
    '''
    if 'file' not in request.files:
        return {'success': False, 'message': '没有选择文件'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'success': False, 'message': '没有选择文件'}, 400

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {
            'success': True,
            'message': '文件上传成功',
            'filename': filename
        }, 200

@app.route('/download/<filename>')
def download_file(filename):
    '''下载文件'''
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True  # 添加这个参数强制下载而不是在浏览器中打开
    )

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {'success': True, 'message': '文件删除成功'}, 200
        return {'success': False, 'message': '文件不存在'}, 404
    except Exception as e:
        return {'success': False, 'message': str(e)}, 500


# 获取目录下所有文件的API 和 文件上传API
# 自动区分POST和GET请求
class FILES_LIST(Resource):
    def get(self):
        try:
            files = os.listdir(app.config['UPLOAD_FOLDER'])
            return {
                'success': True,
                'message': '文件列表获取成功',
                'files': files
            }, 200
        except Exception as e:
            return {
                'success': False,
                'message': f'获取文件列表失败: {str(e)}'
            }, 500

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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

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

api.add_resource(FILES_LIST,'/api/v1/files')
# api.add_resource(FILES_LIST,'/api/v1/post_file')



if __name__ == '__main__':
    app.run(debug=True)