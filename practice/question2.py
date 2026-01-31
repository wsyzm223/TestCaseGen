# 方法二：迭代扩展
def expand_bindings_iteratively(self, base_data):
    """迭代扩展多层绑定关系"""
    # 使用队列进行BFS扩展
    to_expand = [base_data]
    expanded = []

    while to_expand:    # 这里是以是否还存在待扩展数据作为循环的判断标准的
        current_data = to_expand.pop(0)

        # 检查是否还有未处理的绑定
        all_expanded = True
        for bind_parent, bind_child in self.factor_bind.items():
            # 如果这个绑定关系还没处理
            if bind_child in current_data and current_data[bind_child] == '':
                all_expanded = False
                parent_value = current_data[bind_parent]   # 这是 'HK'

                try:
                    child_values = \
                    self.config_normalized[bind_parent][bind_child][
                        parent_value]
                except KeyError:
                    child_values = [current_data.get(bind_child, '')]   # 既然绑定应该有枚举的，没有的话就给空

                # 为每个子值创建新数据
                for child_value in child_values:
                    new_data = current_data.copy()
                    new_data[bind_child] = child_value
                    to_expand.append(new_data)

                break  # 每次只处理一个绑定关系

        if all_expanded:
            expanded.append(current_data)

    return expanded


def bind(original_data):
    to_expend = original_data.copy()        # [original_data] 和 original_data.copy() 有何区别
    expended = []

    while to_expend:
        current_data = to_expend.pop(0)
        # print(f"current_data:{current_data}")
        all_expended = True
        for bind_item in self.factor_bind:
            (parent_name,child_name), = bind_item.items()
            if child_name not in current_data or current_data[child_name] == '':
                all_expended = False
                parent_value = current_data[parent_name]
                try:
                    child_value = self.config_normalized[parent_name][child_name][parent_value]
                except KeyError:
                    print(f"警告: 配置中没有 {parent_name}[{parent_value}] -> {child_name} 的映射")
                    child_value = []
                for child in child_value:
                    data = current_data.copy()
                    data[child_name] = child
                    to_expend.append(data.copy())

            if not all_expended:         # 当已经执行过一次时（all_expected 置为 False）
                break

        if all_expended:
            expended.append(current_data)

    return expended


