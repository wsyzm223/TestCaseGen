"""
一个测试数据生成器
1. 体现了因子交叉组合的思想
2. 根据 age 的边界值配置自动确定需要生成多少数据，生成并输出、检验数据合法性
3. 支持统计共生成了多少组测试数据，并标注ID
"""

# 扩展一：生成数据的 key 不是硬编码，而是根据 config 来
# 扩展二：可配置 组合、交叉、部分因子组合部分因子交叉 三种类型
# 扩展三：做成有界面，可填充、固化、长按调整顺序的形式
# 扩展四：能直接生成 .xmind 文件 （或者生成 excel 再通过脚本转为 .xmind)

# 【想法】 JSON 如何设计才能表达出要表达的全部意思？
# 想法：  券商类型（单券商、多券商）、券商（港美澳新日加马）、市场类型（单市场、多市场）、市场（港美A新澳日加马）、币种（HKD、USD、AUD、SGD、CNH）、
# 方向（买入、卖出、卖空、买回）、标的类型（正股、期权、期货）、
# 想法：  读取现有测试账户类型，进行 prefer 组合测试


from datetime import datetime
from config import DEFAULT_CONFIG

class TestDataGenerator:
    count = 0
    """测试数据生成器，具备如下功能：包含边界值的生成、数据检查、确保配置一致性"""
    def __init__(self,config=None):
        """初始化配置"""
        if config is None:
            self.config = DEFAULT_CONFIG.copy()
        else:
            self.config = config.copy()

        # 生成测试数据
        self.generate_id = TestDataGenerator.count + 1
        print(f"开始生成 ID = {self.generate_id} 的数据")
        self.users = self.generate_test_data()    # 之前这里调用传多了 self，在三个函数都是如此，还不太明白
        self.time = datetime.now()
        print(f"{self.time} 共生成测试数据 {self.count}条：")
        for user in self.users:
            print(user)

        # 检验测试数据
        res, errors = self.validate_test_data()
        if res:
            print("所有数据验证通过.")
        else:
            print(f"共有{len(errors)}个错误：")
            for error in errors:
                print(error)


    @classmethod
    def increase_count(cls):
        """统计调用了多少次生成测试数据的操作"""
        cls.count += 1

    def generate_test_data(self):
        """生成测试数据"""
        users = []
        ages = self.generate_ages()
        self.count = len(ages)
        direction = self.config['direction']

        # 测试数据生成
        for i in range(self.count):
            user = {
                "id": i + 1,
                "name": f"user_{i + 1}",
                "email": f"user_{i + 1}@{self.config['domains'][i % len(self.config['domains'])]}",
                "age": ages[i],
                "direction": direction[i%len(direction)]
            }
            users.append(user)
        return users

    def generate_ages(self):
        """生成ages边界值数据"""
        min_age = self.config['min_age']
        max_age = self.config['max_age']
        ages = []
        ages.append(min_age)
        ages.append(max_age)
        ages.append((max_age + min_age) // 2)
        if self.config["age_if_include_boundary"] == True:
            for offset in self.config["age_boundary_offsets"]:
                if offset != 0:
                    ages.append(min_age + offset)
                    ages.append(max_age + offset)
        TestDataGenerator.increase_count()
        return ages

    def validate_test_data(self):
        """验证测试数据有效性"""
        errors = []
        required_data = ['id', 'name', 'email', 'age']
        for user in self.users:
            # 检查必填字段
            for data in required_data:
                if data not in user:
                    errors.append(f"{user['id']} 不包含 {data} 字段.")
            # 检查年龄范围
            if "age" in user and not (
                    self.config["min_age"] <= user["age"] <= self.config["max_age"]):
                errors.append(f"ID:{user['id']} age 不在范围内.")

        return len(errors) == 0, errors


test_data_1 = TestDataGenerator(DEFAULT_CONFIG)