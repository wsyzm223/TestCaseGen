def yuesefusi_practice(people_num, k):
    if people_num > 0:
        people_list  = list(range(1,people_num+1))
        count = 1         # 计数器
        people_index = 0  # 当计数器为1时，第一个人下标为0
        kill_count = 0    # 杀人计数
        while len(people_list) > 1:
            if count == k:
                killed = people_list.pop(people_index)
                kill_count += 1
                print(f"第{kill_count}轮，{killed}出局")
                count = 1                                  # 错误二：这行没写
            else:
                people_index = (people_index+1) % len(people_list)
                count += 1                                     # 错误一：这行没写
        return people_list[0]
    elif people_num == 0:
        return 0
    else:
        return 'ERROR'

def yuesefusi_practice_0130(people_count,k):
    if people_count > 1:
        people_list = list(range(1,people_count+1))
        count = 1
        people_index = 0
        kill_count = 0
        while len(people_list) > 1:
            if count == k:
                killed = people_list.pop(people_index)
                kill_count += 1
                print(f"第{kill_count}轮，{killed}出局")
                count = 1
                people_index = people_index%len(people_list)   # 之前的解法没有这一行，当 people_count=k 时无法实时表示 index 的正确值，但是也没关系，下次循环就会重置到正确的值，而 k=1 的情况则不可能有机会移动到列表末尾
            else:
                count += 1
                people_index = (people_index + 1) % len(people_list)
        return people_list[0]
    elif people_count == 1:
        return 1
    else:
        return "Input False"


print(yuesefusi_practice(4,2))
print(yuesefusi_practice_0130(4,2))


