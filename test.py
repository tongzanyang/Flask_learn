# @Version  : 1.0
# @Author   : 故河
from PIL import Image, ImageDraw, ImageFont
def add_num(img):
    draw = ImageDraw.Draw(img)
    fillcolor = "#ff0000"
    width, height = img.size
    draw.text((width-50, 5), '@故河', fill=fillcolor)
    img.save('result.jpg','jpeg')
    return 0

if __name__ == '__main__':
    image = Image.open(r"C:\Users\童赞旸\OneDrive\图片\jmbz10.jpg")
    add_num(image)
    image.show()