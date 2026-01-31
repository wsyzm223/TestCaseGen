"""
我在算法书上看到了约瑟夫问题，39人按序坐，每数到7杀掉一人，然后继续。约瑟夫是个数学家，他很快计算好了站位并且成为最终活下来的人。
这个小故事激起了我类似于我父亲跟我讲的“吃饺子故事”的恐慌。所以我迫不及待地想知道排在第几位可以活到最后？
所以我写了这个函数，但是我发现我无法确定我的哪种写法是对的，我已经知道写法三不对，但是我不知道怎么改，而且我觉得我对变量的含义模糊不清。
这体现了我编程中哪些思维漏洞？如何解决？
"""
def yuesefu():
    people = list(range(1,40))
    print(people)
    count = 0
    people_index = 0
    kill_count = 0
    while len(people) > 1:
        count += 1
        # people_index = count%len(people)-1        【写法一】
        people_index += 1                        #  【写法二】
        if people_index > len(people)-1:
            people_index = people_index%len(people)
        if count%7 == 0:
            kill_count += 1
            print(f"第 {kill_count}轮，count = {count}，{people[people_index]} 被杀")
            people.pop(people_index)
    print(people)

# 你知道吗，我总在绕圈子，我把写法二改了一下，似乎能生成正确结果，但是我更懵了，我根本不知道怎样是正确的
# 状态机思维怎么培养
def yuesefu_1():
    people = list(range(1,40))
    print(people)
    count = 0
    people_index = 0
    kill_count = 0
    while len(people) > 1:
        count += 1
        # people_index = count%len(people)-1        【写法一】
        if count%7 == 0:
            kill_count += 1
            killed = people.pop(people_index)
            print(f"第 {kill_count}轮，count = {count}，{killed} 出局")
            people_index -= 1       # 实际应该不往前走，这里预先-1

        people_index = (people_index+1)%len(people)   # 【写法二】
    print(people)


#  【写法三】
def yuesefu_2():
    people = list(range(1,40))
    print(people)
    count = 0
    kill_count = 0
    while len(people) > 1:
        count += 1
        people_index = count%len(people)-1
        if count%7 == 0:
            kill_count += 1
            print(f"第 {kill_count}轮，count = {count}，{people[people_index]} 被杀")
            people.pop(people_index)
            count = 0
    print(people)


def visualize_josephus(n=5, step=3):
    people = list(range(1, n + 1))
    current = 0
    round_num = 1

    print(f"初始: {people}")
    print(f"索引: {list(range(n))}")
    print()

    while len(people) > 1:
        # 计算要删除的位置
        delete_idx = (current + step - 1) % len(people)

        print(f"第{round_num}轮:")
        print(f"当前指向: 人{people[current]} (索引{current})")
        print(f"计算: ({current} + {step} - 1) % {len(people)} = {delete_idx}")
        print(f"删除: 人{people[delete_idx]} (索引{delete_idx})")

        # 删除
        people.pop(delete_idx)

        # 下一轮从被删位置开始
        current = delete_idx % len(people) if people else 0

        print(f"剩余: {people}")
        print(
            f"下一轮从: 人{people[current] if people else '无'} (索引{current})")
        print("-" * 30)
        round_num += 1

    print(f"\n幸存者: {people[0] if people else '无'}")


def josephus_solution():
    people = list(range(1, 40))  # 1到39号
    current_index = 0  # 当前指向的人的索引
    step = 7  # 每数7个

    print("初始顺序:", people)

    kill_count = 0
    while len(people) > 1:
        # 找到要删除的位置：(当前索引 + step - 1) % 当前人数
        # 减1是因为从当前位置开始数，数到step时，实际移动了step-1步
        delete_index = (current_index + step - 1) % len(people)

        kill_count += 1
        print(f"第{kill_count}轮: {people[delete_index]} 出局")

        # 删除这个人
        people.pop(delete_index)

        # 下一轮从被删位置开始（注意：删除后，delete_index位置已经是下一个人）
        current_index = delete_index % len(people)  # 取模防止越界

    print(f"\n最后存活的是: {people[0]}号")
    return people[0]

# 这个AI写的，不对，不用看了
def yuesefu_fixed():
    people = list(range(1, 40))
    count = 0
    current_index = 0  # 当前指向的人
    kill_count = 0

    while len(people) > 1:
        count += 1

        # 模拟报数：移动到下一个人
        current_index = (current_index + 1) % len(people)

        # 如果报数是7的倍数
        if count % 7 == 0:
            kill_count += 1
            # 注意：因为current_index已经移动到了要杀的人
            killed = people.pop(current_index)
            print(f"第{kill_count}轮：{killed}被杀，剩余{len(people)}人")
            # 关键调整：杀掉当前人后，下一个人自动占据了当前位置
            # 所以current_index不需要再移动

    print(f"幸存者：{people[0]}")
    return people[0]


# 运行看看
# yuesefu()
# yuesefu_1()
# yuesefu_fixed()
# josephus_solution()
# # visualize_josephus(5, 3)

def yuesefu_after_ai(people_list,k):
    count = 1     # 计数
    people_index = 0   # 指向的人下标，count=1 时，已经指向了第一个人
    kill_count = 0     # 杀人计数
    while len(people_list) > 1:
        if count == k:
            kill_count += 1
            killed = people_list.pop(people_index)
            print(f"第 {kill_count} 轮，{killed} 被杀")
            count = 0
        else:
            people_index = (people_index+1)%len(people_list)      # 杀了人，原本的下标不需要变。否则需要自增，并且可能人数有变所以取模
        count += 1
    return people_list[0]

print(yuesefu_after_ai(list(range(1,40)),7))