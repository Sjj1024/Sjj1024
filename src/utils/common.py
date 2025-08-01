import math
from PIL import Image, ImageFont, ImageDraw


def json_pic(json: dict):
    print(f"将Json转为图片")
    font_conf = {
        'type': 'simkai.ttf',
        'size': 30,
        'rgb': tuple([0, 0, 0])
    }
    bg_conf = {
        'rgb': tuple([255, 255, 255])
    }
    font = ImageFont.truetype(font_conf['type'], font_conf['size'])
    pic_size = [500, 1000]
    # create new picture
    pic = Image.new('RGB', pic_size, bg_conf['rgb'])
    draw = ImageDraw.Draw(pic)
    i = 1
    for (key, val) in json.items():
        # draw lines
        draw.text((50, 50*i), val, font_conf['rgb'], font)
        i += 1
    # if pic_path:
    #     pic.save(pic_path)
    pic.show()


def exec_jisuan():
    str = "88 + 10"
    res = eval(str)
    print(res)


def get_value():
    print("获取dict的值")
    form = {
        "name": "1",
        "age": "2"
    }
    value_list = list(form.values())
    print(value_list)


def list_add():
    list1 = ["a", "b", "c", "d"]
    list2 = ["e", "f", "g", "h"]
    list3 = [*list1, *list2]
    print(list3)


if __name__ == '__main__':
    # list_add()
    json_str = {
        "mail_host": "smtp.163.com",
        "mail_user": "lanxingsjj@163.com",
        "mail_pass": "QULRMYHTUVMHYVGM",
        "sender": "lanxingsjj@163.com"
    }
    json_pic(json_str)
