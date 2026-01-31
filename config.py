# env_local 添加进入 git.ignore

# config 里面不用写 id，自动自增 testcase id
# type 的类型：intersection、combine、bind 分别代表什么意思
# 如果没有 enumerate 必须有 max_value、min_value，offset_boundary 可选，存在就会按照这个生成，不存在就只有最大最小值中间值 三个数
# bind 类型不需要 enumerate

DEFAULT_CONFIG = {
    "max_age": 65,
    "min_age": 18,
    "age_if_include_boundary": True,
    "age_boundary_offsets": [-1, 0, 1],  # 待开发：关于这一行的配置 + 配置一致性方案四；学习方案五
    "domains": ["test.com", "example.com", "demo.org"],
    "direction": ['buy', 'sell']
}

test_config_1 = {
    "bull_type": {"type": "intersection", "enumerate": ['single', 'multi']},
    "bull_fact": {"type": "intersection",
                  "enumerate": ['HK', 'SG', 'US', 'AU', 'JP', 'CA', 'MA']},
    "market_type": {"type": "intersection", "enumerate": ['single', 'multi']},
    "market_fact": {"type": "intersection",
                    "enumerate": ['HK', 'CN', 'SG', 'US', 'AU', 'JP', 'CA',
                                  'MA']}
}

# 是不是要把 type 名字改得更专业一点？比如 single（单因子组合）、正交

# 需求一：需要 sequence 这个值来确定因子的组合顺序
# 需求二：需要分辨 不同因子的类型，是 increment、intersection、combine 有不同的组合方式，这种可以放同一个函数里面
#       需要 return 这个因子本身的 list，还有 count 乘数：combine 的乘数就是 len，intersection 是取全部 intersection 因子的最大值
#       % 谁？
# 需求三：如果是不交叉不组合，要求挂在一个位置下面全量，其余位置抽测，如何配置？
# intersection 使用 % 组合
# combine 使用一个 for

test_config_2 = {
    "id": {'sequence': 1, 'type': 'increment', 'start': 1},
    "broker": {
        "sequence": 2,
        "type": "intersection",
        "enumerate": ['HK', 'SG', 'US', 'AU', 'JP', 'CA', 'MA'],
        "market": {
            'HK': ['港股', '美股', 'A股'],
            'SG': ['星股', '美股', '港股', 'A股'],
            'US': ['美股', '港股', 'A股', '日股'],
            'AU': ['澳股', '美股', '港股'],
            'JP': ['日股', '美股'],
            'CA': ['美股', '加股'],
            'MA': ['马股']
        }
    },
    "market": {'sequence': 3,
               'type': 'bind',
               "enumerate": ['港股', 'A股', '星股', '美股', '澳股', '日股',
                             '加股', '马股'],
               "currency":{
                   '港股':['HKD'],
                   'A股':['CNH'],
                   '美股':['USD'],
                   '星股':['SGD','USD'],
                   '澳股':['AUD','USD'],
                   '日股':['JPY','USD'],
                   '加股':['CAD','USD'],
                   '马股':['MYR']
               }
               },
    "subject": {'sequence': 4,
                'type': 'combine',
                "enumerate": ['正股', '期权：单腿、组合', '期货']},
    "currency":{'sequence':5,
                'type':'bind',
                'enumerate':['HKD','USD','CNH','SGD','AUD','CAD','JPY','MYR']
    },
    "amount": {'sequence': 7,
               'type': 'intersection', 'min_value': 1, 'max_value': 100,
               'boundary_offsets': [-1, 0, 1]},
    "direction": {'sequence': 6, 'type': 'combine',
                  'enumerate': ['buy', 'sell']}
}

config_test = {
    "broker": {
        "sequence": 1,
        "type": "intersection",
        "enumerate": ['HK', 'CA'],
        "market": {
            'HK': ['港股', '美股', 'A股'],
            'CA': ['美股', '加股']
        }
    },
    "market": {'sequence': 2, 'type': 'intersection',
               "enumerate": ['港股', 'A股',  '美股',
                             '加股'],
               "currency": {
                   '港股': ['HKD'],
                   'A股': ['CNH'],
                   '美股': ['USD'],
                   '加股': ['CAD', 'USD']
               }
               },
    "currency": {'sequence': 3,
                 'type': 'intersection',
                 'enumerate': ['HKD', 'USD', 'CNH','CAD']
                 }
}


res = sorted(test_config_2.keys(),key=lambda x: test_config_2[x]['sequence'])
print(res)

