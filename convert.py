from PIL import Image
import requests
import os


def download_image(templateid):
    content_b = requests.get(f'https://static.notpx.app/templates/{templateid}.png').content

    with open(f'{templateid}.png', 'wb') as f:
        f.write(content_b)


def get(x, y, templateid):
    if not os.path.exists(f'{templateid}.png'):
        download_image(templateid)

    img = Image.open(f'{templateid}.png').convert('RGB')

    # 将图片大小调整为128x128（如果不是这个大小）
    img = img.resize((128, 128))

    # 获取像素数据
    pixels = img.load()

    # 创建一个二维数组，每个元素是表示颜色的十六进制字符串
    pixel_array = []
    for i in range(128):
        row = {}
        for j in range(128):
            r, g, b = pixels[i, j]
            # 将 RGB 值转换为十六进制颜色字符串 (e.g., "#FF0000" for red)
            row[f"{x + j},{y + i}"] = f"#{r:02X}{g:02X}{b:02X}"
            # row.append(hex_color)
        pixel_array.append(row)

    return pixel_array


if __name__ == '__main__':
    print(get(528, 872, 6989019093))
