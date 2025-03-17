from file_manage import app
from flask import send_from_directory, render_template, request, session, redirect, url_for, flash, jsonify
import os
from file_manage.setting import FILE_DIR, PUBLIC_FILE
from werkzeug.utils import secure_filename

# 文件目录
file_dir = FILE_DIR
# 不登录时显示的文件目录
public_file = PUBLIC_FILE

# 允许的文件类型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 判断用户是否登录
def is_login():
    return 'username' in session

# 首页
@app.route('/')
def index():
    try:
        # 检查用户登录状态
        if is_login():
            # 登录用户显示所有文件
            files = os.listdir(file_dir)
            return render_template('index.html', files=files, logged_in=True)
        else:
            # 未登录用户显示公共文件
            files = os.listdir(public_file)
            return render_template('index.html', files=files, logged_in=False)
    except Exception as e:
        flash(f'获取文件列表失败：{str(e)}', 'error')
        return render_template('index.html', files=[], logged_in=is_login())

# 上传文件
@app.route("/upload", methods=["POST"])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': '没有选择文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': '没有选择文件'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'status': 'error', 'message': '不支持的文件类型'}), 400
        
        filename = secure_filename(file.filename)
        
        if is_login():
            # 登录用户上传文件
            file.save(os.path.join(file_dir, filename))
        else:
            # 未登录用户上传文件
            file.save(os.path.join(public_file, filename))
        
        flash('文件上传成功！', 'success')
        return jsonify({'status': 'success', 'message': '文件上传成功'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'文件上传失败：{str(e)}'}), 500

# 下载文件
@app.route("/download/<filename>")
def download(filename):
    try:
        # 安全检查文件名
        filename = secure_filename(filename)
        
        # 根据登录状态确定文件路径
        if is_login():
            directory = file_dir
            file_path = os.path.join(file_dir, filename)
        else:
            directory = public_file
            file_path = os.path.join(public_file, filename)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            flash('文件不存在！', 'error')
            return redirect(url_for('index'))
        
        # 检查文件是否在允许的目录中
        real_path = os.path.realpath(file_path)
        if not real_path.startswith(os.path.realpath(directory)):
            flash('无权访问该文件！', 'error')
            return redirect(url_for('index'))
        
        try:
            return send_from_directory(
                directory,
                filename,
                as_attachment=True,
                download_name=filename
            )
        except Exception as e:
            app.logger.error(f"文件下载失败: {str(e)}")
            flash('文件下载失败，请重试！', 'error')
            return redirect(url_for('index'))
    
    except Exception as e:
        app.logger.error(f"文件下载出错: {str(e)}")
        flash(f'文件下载失败：{str(e)}', 'error')
        return redirect(url_for('index'))

# 删除文件
@app.route("/delete/<filename>")
def delete(filename):
    if not is_login():
        flash('请先登录！', 'error')
        return redirect(url_for('login'))
    
    try:
        file_path = os.path.join(file_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash('文件删除成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('文件不存在！', 'error')
            return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'文件删除失败：{str(e)}', 'error')
        return redirect(url_for('index'))

# 重命名
@app.route("/rename/<filename>", methods=["POST"])
def rename(filename):
    if not is_login():
        return jsonify({'status': 'error', 'message': '请先登录！'}), 401
    
    try:
        new_filename = request.form.get("new_filename")
        if not new_filename:
            return jsonify({'status': 'error', 'message': '新文件名不能为空'}), 400
        
        new_filename = secure_filename(new_filename)
        old_file_path = os.path.join(file_dir, filename)
        new_file_path = os.path.join(file_dir, new_filename)
        
        if not os.path.exists(old_file_path):
            return jsonify({'status': 'error', 'message': '文件不存在'}), 404
        
        if os.path.exists(new_file_path):
            return jsonify({'status': 'error', 'message': '新文件名已存在'}), 400
        
        os.rename(old_file_path, new_file_path)
        flash('文件重命名成功！', 'success')
        return jsonify({'status': 'success', 'message': '文件重命名成功'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'文件重命名失败：{str(e)}'}), 500