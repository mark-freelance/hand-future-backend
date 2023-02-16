import re

from log import getLogger

logger = getLogger("Regex")


def parse_p1(pattern, text) -> str:
    """
    解析正则匹配里第一个括号里的信息

    :param pattern:
    :param text:
    :return:
    """
    m = re.search(pattern, text)
    if m:
        return m[1]
    else:
        logger.warning(f"not matched from pattern: {pattern}")
        return ""
