# process_data.py

import json
import sys

from field import field
from gen_random import gen_random
from unique import Unique
from print_result import print_result
from cm_timer import cm_timer_1


# 获取命令行参数中的 json 路径
# 例如：python process_data.py data_light.json
if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    # 也可以改成绝对路径或你自己的默认路径
    path = 'data_light.json'

with open(path, encoding='utf-8') as f:
    data = json.load(f)


@print_result
def f1(arg):
    """
    输出：按职业名称排序、去重后的列表
    - 使用 field 取出职业名称 (假设字段是 'job-name')
    - 使用 Unique(ignore_case=True) 去重
    - sorted 时忽略大小写
    """
    return sorted(
        Unique(field(arg, 'job-name'), ignore_case=True),
        key=str.lower
    )


@print_result
def f2(arg):
    """
    过滤：只保留以 'программист' 开头的职业
    """
    return list(filter(lambda s: s.lower().startswith('программист'), arg))


@print_result
def f3(arg):
    """
    修改：在每个职业后面加上 'с опытом Python'
    """
    return list(map(lambda s: f"{s} с опытом Python", arg))


@print_result
def f4(arg):
    """
    为每个职业生成 [100000, 200000] 的随机工资，并拼接成字符串
    """
    salaries = list(gen_random(len(arg), 100000, 200000))
    return [f"{name}, зарплата {salary} руб." for name, salary in zip(arg, salaries)]


if __name__ == '__main__':
    with cm_timer_1():
        f4(f3(f2(f1(data))))
