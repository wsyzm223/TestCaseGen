# test_data_gen.py

from datetime import datetime
from config import DEFAULT_CONFIG
from random import randint


def generate_user_data(count=10, config=None):
    """生成模拟用户数据"""
    if config is None:
        config = DEFAULT_CONFIG

    users = []
    ages = generate_ages(count, config)

    # 测试数据生成
    for i in range(count):
        user = {
            "id": i + 1,
            "name": f"user_{i + 1}",
            "email": f"user_{i + 1}@{config['domains'][i % len(config['domains'])]}",
            "age": ages[i % len(ages)]
        }
        users.append(user)
    return users


def generate_ages(count=10, config=None):
    if config is None:
        config = DEFAULT_CONFIG
    min_age = config['min_age']
    max_age = config['max_age']
    ages = []
    if config["age_if_include_boundary"] == False:
        ages.append(min_age)
        ages.append(max_age)
        ages.append((max_age + min_age) // 2)
    else:
        for i in config["age_boundary_offsets"]:
            ages.append(min_age + i)
            ages.append(max_age + i)
        ages.append((max_age + min_age) // 2)

    while len(ages) < count:
        ages.append(randint(min_age, max_age))
    return ages


def validate_user_date(users, config=None):
    """
        需求：检查一下各个字段都存在
        需求：检查一下age在范围内
        需求：return错误信息
    """

    if config is None:
        config = DEFAULT_CONFIG

    errors = []
    required_data = ['id', 'name', 'email', 'age']
    for user in users:
        # 检查必填字段
        for data in required_data:
            if data not in user:
                errors.append(f"{user['id']} 不包含 {data} 字段.")
        # 检查年龄范围
        if "age" in user and not (
                config["min_age"] <= user["age"] <= config["max_age"]):
            errors.append(f"ID:{user['id']} age 不在范围内.")

    return len(errors) == 0, errors


if __name__ == "__main__":

    my_config = {
        "max_age": 60,
        "min_age": 20,
        "domains": ["futunn.com", "moego.pet"],
        "age_if_include_boundary": True,
        "age_boundary_offsets": [-1, 0, 1],
    }

    config = my_config

    users = generate_user_data(10, config)
    print(f"当前时间：{datetime.now()}")
    print(datetime.ctime(datetime.now()))  # 原来 ctime是个转换函数
    for user in users:
        print(user)
    print('\n数据验证：')

    res, errors = validate_user_date(users, config)
    if res:
        print("所有数据验证通过.")
    else:
        print(f"共有{len(errors)}个错误：")
        for error in errors:
            print(error)
