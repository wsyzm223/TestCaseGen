# 这是我实践我烂代码权的一个脚本
# 计算器，只支持加减乘除和乘方

def calculator(a, operate, b):
    if operate == '^':
        return a ** b
    else:
        return eval(f"{a}{operate}{b}")

def calculator_2(a, operate, b):
    if operate == '+':
        return a+b
    if operate == '-':
        return a-b
    if operate == '*':
        return a*b
    if operate == '/':
        return a/b
    if operate == '^':
        return a**b


test_cases = [
    (1, '+', 2),
    (1, '-', 2),
    (1, '*', 2),
    (1, '/', 2),
    (2, '^', 4),
]

for i in test_cases:
    assert calculator(*i) == calculator_2(*i)
