import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os


def check_code(width=180, height=100, char_length=4, font_file='', font_size=40):
    """
    生成大字体验证码
    """
    code = []
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """生成随机字符 - 增加数字选项"""
        char_type = random.randint(0, 2)
        if char_type == 0:
            return chr(random.randint(ord('A'), ord('Z')))  # 大写字母
        elif char_type == 1:
            return chr(random.randint(ord('a'), ord('z')))  # 小写字母
        else:
            return chr(random.randint(ord('0'), ord('9')))  # 数字

    def rndColor():
        """生成随机颜色"""
        return (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))

    def rndBgColor():
        """生成随机背景颜色"""
        return (random.randint(180, 255), random.randint(180, 255), random.randint(180, 255))

    # 设置背景色
    bg_color = rndBgColor()
    draw.rectangle((0, 0, width, height), fill=bg_color)

    # 生成验证码字符
    for i in range(char_length):
        char = rndChar()
        code.append(char)

    # 字体处理 - 优先使用系统字体
    font = None
    font_paths = [
        font_file,
        '/System/Library/Fonts/Arial.ttf',  # macOS
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux
        'C:/Windows/Fonts/arial.ttf',  # Windows
    ]

    for path in font_paths:
        if path and os.path.exists(path):
            try:
                font = ImageFont.truetype(path, font_size)
                break
            except:
                continue

    # 如果找不到字体文件，使用默认字体（放大）
    if font is None:
        try:
            font = ImageFont.load_default()
        except:
            # 创建简单的位图字体
            font = ImageFont.load_default()

    # 绘制验证码字符（先绘制字符，再绘制干扰）
    char_positions = []
    for i, char in enumerate(code):
        # 计算字符位置，确保不超出边界
        char_width = font_size * 0.8
        x = width * 0.1 + i * (width * 0.8 / char_length) + random.randint(-5, 5)
        y = random.randint(5, height - font_size - 5)
        char_positions.append((x, y, char))

    # 绘制字符
    for x, y, char in char_positions:
        draw.text((x, y), char, font=font, fill=rndColor())

    # 绘制干扰点（在字符后面）
    for i in range(20):  # 减少干扰点数量
        draw.point([random.randint(0, width), random.randint(0, height)],
                   fill=rndColor())

    # 绘制干扰线（细线，不遮挡字符）
    for i in range(3):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor(), width=1)

    # 轻微模糊
    img = img.filter(ImageFilter.SMOOTH)

    code_str = ''.join(code)
    return img, code_str