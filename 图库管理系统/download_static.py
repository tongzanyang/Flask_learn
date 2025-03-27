# 下载相关的样式文件和js文件

import os
import requests
import shutil

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {filename}")

def main():
    # 创建必要的目录
    os.makedirs('picture_system/static/css', exist_ok=True)
    os.makedirs('picture_system/static/js', exist_ok=True)
    os.makedirs('picture_system/static/fonts', exist_ok=True)

    # 下载 Bootstrap CSS
    download_file(
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
        'picture_system/static/css/bootstrap.min.css'
    )

    # 下载 Bootstrap JS
    download_file(
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
        'picture_system/static/js/bootstrap.bundle.min.js'
    )

    # 下载 jQuery
    download_file(
        'https://code.jquery.com/jquery-3.6.0.min.js',
        'picture_system/static/js/jquery.min.js'
    )

    # 下载 Font Awesome
    download_file(
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
        'picture_system/static/css/all.min.css'
    )

    # 下载 Font Awesome 字体文件
    font_files = [
        'fa-solid-900.woff2',
        'fa-solid-900.woff',
        'fa-solid-900.ttf',
        'fa-solid-900.eot',
        'fa-solid-900.svg'
    ]
    
    for font_file in font_files:
        download_file(
            f'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/{font_file}',
            f'picture_system/static/fonts/{font_file}'
        )

if __name__ == '__main__':
    main() 