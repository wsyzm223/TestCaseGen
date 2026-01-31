# 任务1：写一个温度转换器
# 要求：每个变量只有一个职责

def temperature_converter():
    # 变量1：存储输入的温度值（职责：原始数据）
    input_temp = float(input("请输入温度: "))

    # 变量2：存储单位（职责：原始单位）
    input_unit = input("请输入单位(C/F): ").upper()

    # 变量3：存储转换后的温度（职责：结果）
    converted_temp = 0.0

    # 变量4：存储目标单位（职责：目标单位）
    converted_unit = ""

    if input_unit == "C":
        converted_temp = input_temp * 9 / 5 + 32
        converted_unit = "F"
    else:
        converted_temp = (input_temp - 32) * 5 / 9
        converted_unit = "C"

    # 变量5：存储格式化后的输出（职责：展示）
    result_str = f"{input_temp}{input_unit} = {converted_temp:.1f}{converted_unit}"

    print(result_str)

# 测试你的理解：每个变量的职责是什么？能改名使其更清晰吗？

temperature_converter()





# 任务2：计算购物车总价
# 要求：区分"数据变量"和"计算变量"

def shopping_cart_calculator():
    # 数据变量组（职责：存储原始数据）
    item_prices = [10.99, 5.49, 7.99, 12.50]  # 职责：商品价格列表
    quantities = [2, 3, 1, 2]  # 职责：商品数量列表
    tax_rate = 0.08  # 职责：税率

    # 计算变量组（职责：存储中间计算结果）
    subtotal = 0.0  # 职责：税前总额
    tax_amount = 0.0  # 职责：税费
    total = 0.0  # 职责：税后总额

    # 计算逻辑
    for i in range(len(item_prices)):
        subtotal += item_prices[i] * quantities[i]

    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount

    # 输出变量组（职责：格式化展示）
    output_lines = [
        f"商品明细: {len(item_prices)} 种商品",
        f"税前总额: ${subtotal:.2f}",
        f"税费 (8%): ${tax_amount:.2f}",
        f"总计: ${total:.2f}"
    ]

    for line in output_lines:
        print(line)

# 练习：尝试给每个变量添加单行注释，明确其职责



# 任务3：管理待办事项
# 要求：区分"状态变量"和"操作变量"

def simple_task_manager():
    # 状态变量（职责：描述系统当前状态）
    tasks = ["买菜", "写代码", "锻炼"]  # 职责：存储所有任务
    current_task_index = 0  # 职责：当前正在处理的任务索引
    is_completed = [False, False, False]  # 职责：任务完成状态

    # 操作变量（职责：临时存储操作相关数据）
    user_choice = ""  # 职责：用户选择
    task_to_add = ""  # 职责：要添加的任务

    while True:
        # 展示变量（职责：临时存储展示内容）
        status_summary = f"当前任务: {tasks[current_task_index]}"
        completion_status = "✓" if is_completed[current_task_index] else "✗"

        print(f"\n{status_summary} [{completion_status}]")
        print("1. 标记完成 2. 下一个任务 3. 添加任务 4. 退出")

        user_choice = input("请选择: ")

        if user_choice == "1":
            is_completed[current_task_index] = True
        elif user_choice == "2":
            current_task_index = (current_task_index + 1) % len(tasks)
        elif user_choice == "3":
            task_to_add = input("输入新任务: ")
            tasks.append(task_to_add)
            is_completed.append(False)
        elif user_choice == "4":
            break

    # 统计变量（职责：存储最终统计结果）
    completed_count = sum(is_completed)
    total_count = len(tasks)

    print(f"\n完成 {completed_count}/{total_count} 个任务")


# 任务4：重构这段混乱的代码
# 要求：给每个变量明确的单一职责

def messy_code_refactoring():
    # 原始混乱的代码
    age = 10  # 这个变量有三个职责：既是年龄，又是分数，还是计数器
    count = 10
    score = 10
    num = 5  # 这个变量有两个职责：既是数量，又是系数
    coefficient = 5

    # 它做了三件事：
    score_all = score * num  # 1. 计算总分
    print(f"总分: {score_all}")

    age_new = age + 1  # 2. 年龄增长
    print(f"新年龄: {age_new}")

    num_new = num - 1  # 3. 数量减少
    print(f"剩余数量: {num_new}")

    # 你的任务：重写这段代码，让每个变量只有一个职责
    # 提示：需要至少定义4个不同的变量

    # 开始你的重构...


# 练习：为以下场景选择最佳命名
scenarios = {
    "1. 存储用户输入的用户名": [
        "user_input_name",   # 我选择这个，最直观，而且name位于最后
        "input_user_name",   # 体现了变量是name，但是动词在前，不太好
        "name_from_user",    # name在最前面，不太合适
        "username_input"     # 动词结尾，像是个函数名，不是变量名
    ],

    "2. 存储计算后的商品总价": [
        "calculated_total_price",   # 我选择这个，因为既体现了计算后的，又体现了是商品总价
        "total_price_calculated",   # total_price 在前面，不太合适
        "final_product_price",      # final 不如 calculated 具体
        "price_total_final"         # 很混乱
    ],

    "3. 存储从数据库查询的用户列表": [
        "users_from_database",   # users在最前面，不太合适
        "database_users",        # 这个看起来像是直接从数据库里取出来的，没有查询这个动作
        "queried_users_list",   # 我选择这个，因为queried本身隐含从数据库查询出来的意思，users_list标明了它的性质
        "user_query_results"    # 老问题，user在前了
    ]
}

# 你的选择是什么？为什么？
# 试着写出每个命名的优缺点