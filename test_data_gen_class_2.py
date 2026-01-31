"""
一个测试数据生成器
1. 根据 JSON 按照配置项，支持因子 组合覆盖、交叉覆盖、重点位置全量+其他位置抽测 的不同配置
2. 根据因子边界值配置生成枚举生成并输出、检验数据合法性
3. 支持统计共生成了多少组测试数据，并标注ID
"""

# 【01.28 donelist】
# zip、isinstance(collections.abc.Iterable/Interator/Generator) 判断是否是可迭代对象、迭代器、生成器
# collections defaultdict 的用法
# 变量职责不清、状态机 练习

# 【明日计划】
# 3. 需求：使用 collections 实现有序字典 OrderedDict
# 4. 需求：规范化命名（已采用 data 系）：intersection_datas / binded_datas / datas  【DONE】
# 5. 需求：对于多个存在异常值的因子，需要组合，而且是在特定分支上扩展异常值

# 存在绑定关系的也可以没有 enumerate 属性
# 没有映射的，需要处理在最终 error 里面

# 01/24
# 需求一：检测为异常数据的不扩展，如 amount = 0/101：利用 validate 函数在生成笛卡尔积组合时检查       【DONE】 25min
# 需求二：能读懂 config 里的依赖，如 broker - market 的绑定关系
#       1. 根据 sequence 这个字段依次检查，不用写两层 for
#       2. 它在交叉之前还是之后？之前的话怎么写？  - 先识别 broker 能否全覆盖，识别后 market 的 type 失效，不作为交叉的材料，交叉之后，笛卡尔之前
#       3. 现在先实现个一层绑定？多层绑定怎么办？      【DONE】 1h

# 需求三：边界值如何处理，让用例比较平衡，至少每个分支 amount 都有测到正常值？
# 需求四：我可能要思考重构一下，现在变量名什么的很乱

# 需求五：针对期权 能发出单腿、组合的分支        【可能要重新设计JSON】
# 需求六：规范化命名
# 需求七：上 github
# 学习一：itertools.product 实现原理

# 01/22
# 扩展一：生成数据的 key 不是硬编码，而是根据 config 来
# 扩展二：可配置 组合、交叉、部分因子组合部分因子交叉 三种类型
# 扩展三：做成有界面，可填充、固化、长按调整顺序的形式
# 扩展四：能直接生成 .xmind 文件 （或者生成 excel 再通过脚本转为 .xmind)

# 【想法】 01/22
# 1. JSON 如何设计才能表达出要表达的全部意思？
# 2. 允许部分定制化 + 读取现有账户类型，比如 multi-broker 就是 港+美+A

# 想法：  券商类型（单券商、多券商）、券商（港美澳新日加马）、市场类型（单市场、多市场）、市场（港美A新澳日加马）、币种（HKD、USD、AUD、SGD、CNH）、
# 方向（买入、卖出、卖空、买回）、标的类型（正股、期权、期货）、



from datetime import datetime
import config
import itertools
from collections import OrderedDict



class TestCasesGenerator:
    count = 0
    """测试用例生成器，具备通过复杂因子组合生成测试用例的功能。包含边界值的生成、数据检查、确保配置一致性"""

    def __init__(self, config=None):
        """初始化配置"""

        # 判空
        if config is None:
            self.config = config.DEFAULT_CONFIG.copy()
        else:
            self.config = config.copy()


        # 确认组合顺序
        all_have_sequence = all('sequence' in v for v in self.config.values())    # 【重点】这行代码是AI写的，我能读懂但是我自己写不出，感觉脑子里没字典结构
        if all_have_sequence:
            config_keys = self.config.keys()
            self.factors = sorted(config_keys,
                                  key=lambda x: self.config[x]['sequence'])    # 【重点】这行代码之前写错了，写成了 self.config_keys[x]['sequence']，充分说明对字典理解不到位
            print(self.factors)
        else:
            raise Warning("配置 JSON没有指定顺序，可能导致生成错误")


        # 规范化config
        self.count = 1
        self.config_normalize()
        print(self.config_normalized)


        # 生成测试数据
        self.generate_id = TestCasesGenerator.count + 1
        print(f"开始生成 ID = {self.generate_id} 的数据")
        self.datas = self.generate_test_data()     # 之前这里调用传多了 self，在三个函数都是如此，还不太明白
        self.time = datetime.now()
        print(f"{self.time} 共生成测试数据 {self.count}条：")
        for data in self.datas:
            print(data)

    def config_normalize(self):
        """对所有有价值因子填充枚举，为最终用例生成做准备"""
        config_normalize = self.config.copy()
        self.config_enumerate_gen = {}
        for factor,factor_value in config_normalize.items():
            if factor_value['type'] != 'increment':
                if 'enumerate' not in factor_value:
                    if 'min_value' in factor_value and 'max_value' in factor_value:
                        self.config_enumerate_gen[factor] = factor_value
                        min_value = factor_value['min_value']
                        max_value = factor_value['max_value']
                        factor_enumerate = []
                        factor_enumerate.append(min_value)
                        factor_enumerate.append(max_value)
                        if isinstance(min_value, int) and isinstance(
                                max_value, int):
                            factor_enumerate.append(
                                (min_value + max_value) // 2)
                        else:
                            factor_enumerate.append(
                                (min_value + max_value) / 2)
                        if 'boundary_offsets' in factor_value:
                            for offset in factor_value["boundary_offsets"]:
                                if offset != 0:
                                    factor_enumerate.append(min_value + offset)
                                    factor_enumerate.append(max_value + offset)
                        factor_value['enumerate'] = factor_enumerate
                    else:
                        raise ValueError("JSON 格式不正确，没有 enumerate 需要指定 min_value、max_value")
                factor_value['count'] = len(factor_value['enumerate'])
        self.config_normalized = config_normalize
        self.bind_recognize()

    @classmethod
    def increase_count(cls):
        """统计调用了多少次生成测试数据的操作"""
        cls.count += 1


    def generate_test_data(self):
        """生成测试数据"""

        # 规范化 config预处理
        intersection_datas = []
        count_intersection = 1
        expand_fields = []
        expand_values = []
        for factor,factor_value in self.config_normalized.items():
            if factor_value['type'] == 'intersection':
                count_intersection = max(count_intersection,factor_value['count'])
            if factor_value['type'] == 'combine':
                expand_fields.append(factor)
                expand_values.append(factor_value['enumerate'])

        # 先做交叉组合
        for i in range(count_intersection):
            intersection_data = {key: '' for key in self.config_normalized}
            for factor,factor_value in self.config_normalized.items():
                if factor != 'data':
                    if factor_value['type'] == 'intersection':
                        intersection_data[factor] = factor_value['enumerate'][i%len(factor_value['enumerate'])]
            intersection_datas.append(intersection_data)
        print(f"交叉组合得到测试数据 {len(intersection_datas)}条")

        # 识别绑定，做扩展
        binded_datas = self.bind_expend(intersection_datas)
        print(f"绑定关系得到测试数据 {len(binded_datas)}条")
        # print(f"识别到的绑定：{self.factor_bind}")
        # datas_binded = []
        # for data_intersection in datas_intersection:
        #     for bind_items in self.factor_bind:
        #         for bind,binded in bind_items.items():
        #             bind_now = data_intersection[bind]
        #             try:
        #                 binded_now = self.config_normalized[bind][binded][bind_now]       # 我陷入了一个典型的困境
        #             except KeyError:
        #                 print("【问题排查】")
        #                 print(f"当前data {data_intersection}")
        #                 print(f"当前 bind：{bind}  当前 binded：{binded} 当前 bind_now：{bind_now}")
        #             for binded_item in binded_now:
        #                 data = data_intersection.copy()
        #                 data[binded] = binded_item
        #                 datas_binded.append(data.copy())
        #
        # print(f"绑定操作得到测试数据 {len(datas_binded)}条")
        # for i in datas_binded:
        #     print(i)


        # 再做笛卡尔积组合
        value_combinations = list(itertools.product(*expand_values))       # 迭代器只能用一次，转换为列表更方便
        datas = []
        for binded_data in binded_datas:
            binded_data = self.validate_factor(binded_data)
            if 'invalid' not in binded_data or not binded_data['invalid']:       # 异常数据不做笛卡尔积扩展
                original_data = {k:v for k,v in binded_data.items() if k not in expand_fields}
                for combine in value_combinations:
                    expanded_data = dict(zip(expand_fields, combine))
                    data = {**original_data, **expanded_data}          # 字典扩展最佳实践，如两个字典有相同键，取后面字典的值
                    datas.append(data.copy())
            else:
                datas.append(binded_data.copy())

        print(f"笛卡尔积得到测试数据 {len(datas)}条")

        # 最后处理 id 自增的问题
        data_id = 1
        for data in datas:
            data['id'] = str(data_id).zfill(6)
            data_id += 1


        self.count = len(datas)
        return datas


    def bind_recognize(self):
        self.factor_bind = []
        for i in range(len(self.factors)-1):
            for j in range(i+1,len(self.factors)):
                if self.factors[j] in self.config_normalized[self.factors[i]]:
                    # 【重点】这里之前错写成 if self.config_normalized[self.factors[i+1]] in self.config_normalized[self.factors[i]]:
                    self.config_normalized[self.factors[j]]['type'] = 'binded'
                    self.config_normalized[self.factors[i]]['bind'] = 'True'
                    bind_item = {}
                    bind_item[self.factors[i]] = self.factors[j]
                    self.factor_bind.append(bind_item)

    def bind_expend(self, original_data):
        """
        BFS 进行绑定因子扩展
        FIFO 队列天然适合 BFS
        """
        to_expend = original_data.copy()
        expended = []

        while to_expend:         # 错误一：循环停止条件不清，这样下去 to_expend 只进不出，体现一种很老派的控制感，居然能成功运行只是多了几个警告打印是我没想到的
            data = to_expend.pop(0)
            # print(f"正在处理： {data}")
            all_expended = True
            for bind_item in self.factor_bind:
                (parent_name, child_name), = bind_item.items()
                if child_name not in data or data[child_name] == '':
                    all_expended = False
                    parent_value = data[parent_name]
                    try:
                        child_value = self.config_normalized[parent_name][child_name][parent_value]
                    except KeyError:
                        print(f"{parent_name} -> {child_name} 中 {parent_name}={parent_value} 的绑定关系不存在")
                        child_value = []
                    for child in child_value:
                        current_data = data.copy()
                        current_data[child_name] = child     # 错误二：child_name 写成 child_value，体现一个变量不清
                        to_expend.append(current_data.copy())
                # 错误三：没写 break，break 依然没有内化到我脑子里，目前还只是记忆
                if all_expended == False:
                    break
            if all_expended == True:
                expended.append(data.copy())
        return expended


    def validate_factor(self, data):
        """验证测试数据有效性，异常的不进行笛卡尔积扩展"""
        for factor,factor_value in self.config_enumerate_gen.items():
            if data[factor] > factor_value["max_value"] or data[factor] < factor_value["min_value"]:
                data['invalid'] = 'True'
        return data

    def validate_data(self):
        # 针对什么检查？ 交叉、组合、绑定、enumerate_gen？
        factor_intersection = {}
        for factor,factor_value in self.config.items():
            if factor_value['type'] == 'intersection':
                factor_intersection[factor] = 0
            elif factor_value['type'] == 'combine':
                pass



test_data_1 = TestCasesGenerator(config.test_config_2)
