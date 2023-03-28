def _init():  # 初始化
    global _global_dict
    _global_dict = {}
    global _global_mima
    _global_mima = ''

def set_value(key, value):
    #定义一个全局变量
    _global_dict[key] = value


def get_value(key):
    #获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return _global_dict[key]
    except:
        print('读取'+key+'失败\r\n')

def get_mima():
    return _global_mima


def set_mima(mima):
    global  _global_mima
    _global_mima = mima
