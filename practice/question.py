# all、zip、字典推导式
# 笛卡尔积：itertools.product
# 多重绑定关系 BFS



# 问题分解 请你帮忙看下，怎样的代码能通过 datas 和 config 正交扩展生成 datas_res
# datas = [
#     {"broker":"HK", "subject":"", "direction":""},
#     {"broker": "SG", "subject": "", "direction": ""}
# ]
#
# config = {
#     "subject": {"enumerate":['正股', '期权', '期货']},
#     "direction": {"enumerate":["buy", "sell"]}
# }
#
# datas_res = [
#     {"broker":"HK", "subject":"正股", "direction":"buy"},
#     {"broker": "HK", "subject": "正股", "direction": "sell"},
#     {"broker": "HK", "subject": "期权", "direction": "buy"},
#     {"broker": "HK", "subject": "期权", "direction": "sell"},
#     {"broker": "HK", "subject": "期货", "direction": "buy"},
#     {"broker": "HK", "subject": "期货", "direction": "sell"},
#     {"broker": "SG", "subject": "正股", "direction": "buy"},
#     {"broker": "SG", "subject": "正股", "direction": "sell"},
#     {"broker": "SG", "subject": "期权", "direction": "buy"},
#     {"broker": "SG", "subject": "期权", "direction": "sell"},
#     {"broker": "SG", "subject": "期货", "direction": "buy"},
#     {"broker": "SG", "subject": "期货", "direction": "sell"},
# ]

import itertools

# 原始数据
datas = [
    {"broker":"HK", "subject":"", "direction":""},
    {"broker": "SG", "subject": "", "direction": ""}
]

config = {
    "subject": {"enumerate":['正股', '期权', '期货']},
    "direction": {"enumerate":["buy", "sell"]}
}

# 步骤1：提取需要扩展的字段和对应的枚举值
expand_fields = []  # 存储要扩展的字段名，如 ['subject', 'direction']
expand_values = []  # 存储对应字段的枚举值列表，如 [['正股','期权','期货'], ['buy','sell']]
for field, conf in config.items():
    expand_fields.append(field)
    expand_values.append(conf["enumerate"])

# 步骤2：生成所有枚举值的笛卡尔积（正交组合）
value_combinations = itertools.product(*expand_values)

# 步骤3：遍历基础数据，结合枚举组合生成最终结果
datas_res = []
for base_dict in datas:
    # 提取基础字典中的固定字段（如broker），排除待扩展的字段
    fixed_data = {k: v for k, v in base_dict.items() if k not in expand_fields}
    # 遍历每一种枚举组合，生成新字典
    for combo in value_combinations:
        # 把枚举组合转换成 {字段: 值} 的格式
        expand_data = dict(zip(expand_fields, combo))
        # 合并固定字段和扩展字段，生成新字典
        new_dict = {**fixed_data, **expand_data}
        datas_res.append(new_dict)
    # 重置迭代器（因为product返回的迭代器只能遍历一次）
    value_combinations = itertools.product(*expand_values)

# 打印结果验证
for item in datas_res:
    print(item)