import re
from typing import Union, Any

from src.libs.log import getLogger

logger = getLogger("Regex")


def parse_p1(pattern, text: Any, func=str) -> Union[str, None]:
    """
    解析正则匹配里第一个括号里的信息

    :param pattern:
    :param text:
    :param func: 序列化函数
    :return:
    """
    if not text:
        return

    m = re.search(pattern, func(text))
    if m:
        return m[1]
    else:
        logger.debug(f"not matched from pattern: {pattern}")
