import pickle
from mypinyin import Pinyin
import random
import ctypes

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

FOREGROUND_DARKWHITE = 0x07  # 暗白色
FOREGROUND_BLUE = 0x09  # 蓝色
FOREGROUND_GREEN = 0x0a  # 绿色
FOREGROUND_SKYBLUE = 0x0b  # 天蓝色
FOREGROUND_RED = 0x0c  # 红色
FOREGROUND_PINK = 0x0d  # 粉红色
FOREGROUND_YELLOW = 0x0e  # 黄色
FOREGROUND_WHITE = 0x0f  # 白色

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

# 设置CMD文字颜色
def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

# 重置文字颜色为暗白色
def resetColor():
    set_cmd_text_color(FOREGROUND_DARKWHITE)

# 在CMD中以指定颜色输出文字
def cprint(mess, color):
    color_dict = {
                  '蓝色': FOREGROUND_BLUE,
                  '绿色': FOREGROUND_GREEN,
                  '天蓝色': FOREGROUND_SKYBLUE,
                  '红色': FOREGROUND_RED,
                  '粉红色': FOREGROUND_PINK,
                  '黄色': FOREGROUND_YELLOW,
                  '白色': FOREGROUND_WHITE
                 }
    set_cmd_text_color(color_dict[color])
    print(mess)
    resetColor()

color_list = ['蓝色','绿色','天蓝色','红色','粉红色','黄色','白色']

# 获取字典
with open('./poemDict.pk', 'rb') as f:
    poem_dict = pickle.load(f)

#for key, value in poem_dict.items():
    #print(key, value)

MODE = str(input('Choose MODE(1 for 人工接龙, 2 for 机器接龙): '))

while True:
    try:
        if MODE == '1':
            enter = str(input('\n请输入一句诗或一个字开始：'))
            while enter != 'exit':
                test = Pinyin().get_pinyin(enter, tone_marks='marks', splitter=' ')
                tail = test.split()[-1]
                if tail not in poem_dict.keys():
                    cprint('无法接这句诗。\n', '红色')
                    MODE = 0
                    break
                else:
                    cprint('\n机器回复：%s'%random.sample(poem_dict[tail], 1)[0], random.sample(color_list, 1)[0])
                    enter = str(input('你的回复：'))[:-1]

            MODE = 0

        if MODE == '2':
            enter = input('\n请输入一句诗或一个字开始：')

            for i in range(10):
                test = Pinyin().get_pinyin(enter, tone_marks='marks', splitter=' ')
                tail = test.split()[-1]
                if tail not in poem_dict.keys():
                    cprint('------>无法接下去了啦...', '红色')
                    MODE = 0
                    break
                else:
                    answer = random.sample(poem_dict[tail], 1)[0]
                    cprint('（%d）--> %s' % (i+1, answer), random.sample(color_list, 1)[0])
                    enter = answer[:-1]

            print('\n（*****最多展示前10回接龙。*****）')
            MODE = 0

    except Exception as err:
        print(err)
    finally:
        if MODE not in ['1','2']:
            MODE = str(input('\nChoose MODE(1 for 人工接龙, 2 for 机器接龙): '))
