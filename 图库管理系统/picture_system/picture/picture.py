# @Version  : 1.0
# @Author   : 故河
import os
from flask import request, jsonify, current_app, render_template, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from . import picture, Picture, PictureGroup
from . import db
import time


# 允许的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@picture.route('/')
def index():
    """图片管理主页"""
    if 'username' not in session:
        flash('请先登录！', 'error')
        return redirect(url_for('auth.login'))
    
    # 获取用户的所有图片分组
    groups = PictureGroup.query.filter_by(create_user=session['username']).all()
    return render_template('picture/index.html', groups=groups)

@picture.route('/upload', methods=['POST'])
def upload_picture():
    """上传图片"""
    if 'username' not in session:
        return jsonify({'error': '请先登录！'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': '没有文件！'}), 400
    
    file = request.files['file']
    group_id = request.form.get('group_id')
    
    if file.filename == '':
        return jsonify({'error': '没有选择文件！'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 确保文件名唯一
        unique_filename = f"{session['username']}_{int(time.time())}_{filename}"
        
        # 创建用户上传目录
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], session['username'])
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)
        
        # 保存到数据库
        picture = Picture(
            filename=unique_filename,
            original_filename=filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            file_type=file.content_type,
            group_id=group_id,
            upload_user=session['username']
        )
        
        try:
            db.session.add(picture)
            db.session.commit()
            return jsonify({'message': '上传成功！'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': '保存失败！'}), 500
    
    return jsonify({'error': '不支持的文件类型！'}), 400

@picture.route('/pictures')
def get_pictures():
    """获取图片列表"""
    if 'username' not in session:
        return jsonify({'error': '请先登录！'}), 401
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    group_id = request.args.get('group_id', type=int)
    
    query = Picture.query.filter_by(upload_user=session['username'])
    if group_id:
        query = query.filter_by(group_id=group_id)
    
    pagination = query.order_by(Picture.upload_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    pictures = pagination.items
    
    return jsonify({
        'pictures': [{
            'id': p.id,
            'filename': p.original_filename,
            'file_path': url_for('static', filename=f'uploads/{session["username"]}/{p.filename}'),
            'upload_time': p.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
            'group_id': p.group_id
        } for p in pictures],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@picture.route('/picture/<int:picture_id>', methods=['DELETE'])
def delete_picture(picture_id):
    """删除图片"""
    if 'username' not in session:
        return jsonify({'error': '请先登录！'}), 401
    
    picture = Picture.query.get_or_404(picture_id)
    
    if picture.upload_user != session['username']:
        return jsonify({'error': '没有权限删除此图片！'}), 403
    
    try:
        # 删除文件
        if os.path.exists(picture.file_path):
            os.remove(picture.file_path)
        
        # 删除数据库记录
        db.session.delete(picture)
        db.session.commit()
        return jsonify({'message': '删除成功！'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败！'}), 500

@picture.route('/group', methods=['POST'])
def create_group():
    """创建图片分组"""
    if 'username' not in session:
        return jsonify({'error': '请先登录！'}), 401
    
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        return jsonify({'error': '分组名称不能为空！'}), 400
    
    group = PictureGroup(
        name=name,
        description=description,
        create_user=session['username']
    )
    
    try:
        db.session.add(group)
        db.session.commit()
        return jsonify({'message': '创建成功！'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '创建失败！'}), 500

@picture.route('/group/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """删除图片分组"""
    if 'username' not in session:
        return jsonify({'error': '请先登录！'}), 401
    
    group = PictureGroup.query.get_or_404(group_id)
    
    if group.create_user != session['username']:
        return jsonify({'error': '没有权限删除此分组！'}), 403
    
    try:
        # 删除分组下的所有图片
        for picture in group.pictures:
            if os.path.exists(picture.file_path):
                os.remove(picture.file_path)
            db.session.delete(picture)
        
        db.session.delete(group)
        db.session.commit()
        return jsonify({'message': '删除成功！'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败！'}), 500

@picture.route('/rename', methods=['POST'])
def rename_picture():
    """重命名图片"""
    if 'username' not in session:
        return jsonify({'error': '请先登录！'}), 401
    
    picture_id = request.form.get('picture_id')
    new_filename = request.form.get('new_filename')
    
    if not picture_id or not new_filename:
        return jsonify({'error': '参数不完整！'}), 400
    
    picture = Picture.query.get_or_404(picture_id)
    
    if picture.upload_user != session['username']:
        return jsonify({'error': '没有权限重命名此图片！'}), 403
    
    try:
        # 获取文件扩展名
        old_ext = os.path.splitext(picture.original_filename)[1]
        new_ext = os.path.splitext(new_filename)[1]
        
        # 如果新文件名没有扩展名，使用原文件的扩展名
        if not new_ext:
            new_filename = new_filename + old_ext
        
        # 生成新的唯一文件名
        unique_filename = f"{session['username']}_{int(time.time())}_{new_filename}"
        
        # 更新数据库中的文件名
        picture.original_filename = new_filename
        picture.filename = unique_filename
        
        # 重命名实际文件
        old_path = picture.file_path
        new_path = os.path.join(os.path.dirname(old_path), unique_filename)
        os.rename(old_path, new_path)
        picture.file_path = new_path
        
        db.session.commit()
        return jsonify({'message': '重命名成功！'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '重命名失败！'}), 500

@picture.route('/group', methods=['PUT'])
def update_group():
    """修改图片分组"""
    if 'username' not in session:
        return jsonify({'error': '请先登录！'}), 401
    
    group_id = request.form.get('group_id')
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not group_id or not name:
        return jsonify({'error': '参数不完整！'}), 400
    
    group = PictureGroup.query.get_or_404(group_id)
    
    if group.create_user != session['username']:
        return jsonify({'error': '没有权限修改此分组！'}), 403
    
    try:
        group.name = name
        group.description = description
        db.session.commit()
        return jsonify({'message': '修改成功！'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '修改失败！'}), 500
