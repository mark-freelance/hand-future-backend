import random


def gen_random_activation_code():
    """
    生成六位数字
    :return:
    """
    return "".join(str(random.randint(0, 9)) for _ in range(6))
