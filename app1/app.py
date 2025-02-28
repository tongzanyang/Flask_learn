from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制文件大小为16MB

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

if __name__ == '__main__':
    app.run(debug=True)