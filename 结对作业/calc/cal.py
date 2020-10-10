from fractions import Fraction
import random
import check


def trsan_standard(formula):
    """标准的输出格式，将*转换成x /转换成÷ 分数转为真分数"""
    output = str()
    for item in formula:
        if isinstance(item, Fraction):
            # 如果为分数
            output += Cal.trsan_ans(item)
        elif isinstance(item, int):
            # 如果为整型
            output += str(item)
        elif item == '+':
            output += ' ＋ '
        elif item == '-':
            output += ' － '
        elif item == '*':
            output += ' × '
        elif item == '/':
            output += ' ÷ '
        else:
            output += item
    output += ' ＝ '
    return output


class Cal:
    # 计算类
    def formula(op, left, right):
        if op == "+":
            answer = left + right
        elif op == "-":
            answer = left - right
        elif op == "*":
            answer = left * right
        elif op == "/":
            answer = left / right
            # 浮点数转换为分数形式
            if isinstance(answer, float):
                answer = Fraction(left) / Fraction(right)
        return answer

    def get_answer(self):
        num_list = list()
        for formula in self:
            if isinstance(formula, int) or isinstance(formula, Fraction):
                num_list.append(formula)
            else:
                b = num_list.pop()
                a = num_list.pop()
                res = Cal.eval_formula(formula, a, b)
                num_list.append(res)
        return num_list.pop()

    def grad(u_ans, lists):
        correct = list()
        wrong = list()
        length = len(u_ans)
        for i, k, self in zip(range(1, length + 1), u_ans, lists):
            if k == self:
                correct.append(i)
            else:
                wrong.append(i)
        return correct, wrong

    def trsan_ans(self):
        """将分数转换成真分数格式"""
        if (self > 1 or self < -1) and self.denominator != 1:
            a_numerator = self.numerator % self.denominator
            a_denominator = self.denominator
            a_right = Fraction(a_numerator, a_denominator)
            a_left = self.numerator // self.denominator
            result = str(a_left) + '\'' + str(a_right)
        else:
            result = str(self)
        return result


class Node:
    def __init__(self):
        self.type = 0  # 节点类型{初始化为0；数字为1；操作符为2}
        self.op = None  # 运算符
        self.number = None  # 保存结果
        self.right = None  #
        self.left = None  #
        self.op_priority = {'+': 1, '-': 1, '*': 2, '/': 2}

    def get_answer(self):
        if self.type == 2:
            self.left.get_answer()
            self.right.get_answer()
            self.number = Cal.formula(self.op, self.left.number, self.right.number)
        else:
            return

    def get_formula(self):
        formula = list()
        if self.type == 1:
            return [self.number]
        elif self.type == 2:
            # 左子树
            if self.left.type == 2 and self.op_priority[str(self.op)] > self.op_priority[str(self.left.op)]:
                formula.append('(')
                formula += self.left.get_formula()
                formula.append(')')
            else:
                formula += self.left.get_formula()

            # 中间结点
            formula.append(self.op)

            # 右子树
            if self.right.type == 2 and self.op_priority[str(self.op)] >= self.op_priority[str(self.right.op)]:
                formula.append('(')
                formula += self.right.get_formula()
                formula.append(')')
            else:
                formula += self.right.get_formula()
            return formula


class tree:
    def __init__(self):
        self.root = Node()
        self.op_list = ["+", "-", "*", "/"]
        self.type_list = [1, 2]  # 整数:1, 真分数:2
        self.ans_list = list()  # 答案列表
        self.form_list = list()  # 表达式列表
        self.check_list = list()  # 查重列表

    def gen_formula(self, num_range, number):  # 生成随机式子
        i = 0
        degree = random.randrange(2,3)
        while i < number:
            node_list = [self.root]  # 每次生成一个树
            for _ in range(degree):
                node = random.choice(node_list)
                node_list.remove(node)
                node.op = random.choice(self.op_list)[0]  # 确定操作符
                node.type = 2  # 修改type

                node.left = Node()
                node_list.append(node.left)
                node.right = Node()
                node_list.append(node.right)  #
            try:
                for node in node_list:  # 节点生成随机数
                    node.type = 1
                    num_type = random.choices(self.type_list)[0]
                    if num_type == 1:
                        node.number = random.randint(1, num_range)
                    else:
                        node.number = Fraction(random.randint(1, num_range), random.randint(1, num_range))
                # 查重
                num = 0
                self.root.get_answer()
                for num in range(0, i):
                    if Cal.trsan_ans(self.root.number) == self.ans_list[num]:
                        if check.check(trsan_standard(self.root.get_formula()), self.form_list[num]): #存在返回T
                            num = -1
                            break
                if num > -1:
                    output = trsan_standard(self.root.get_formula())  # 格式化前缀表达式
                    if isinstance(self.root.number, Fraction):
                        answer = Cal.trsan_ans(self.root.number)  # 格式化答案
                    else:
                        answer = self.root.number
                    self.form_list.append(output)
                    self.ans_list.append(answer)
            except ZeroDivisionError:
                continue
            else:
                i += 1
        return self.form_list, self.ans_list
