import os
import sys
import argparse
import cal


def write_file(expr_set, ans_set, exp_file, ans_file):
    index = 0
    with open(exp_file, 'w+', encoding='utf-8') as ef, \
            open(ans_file, 'w+', encoding='utf-8') as af:
        ef.write('题号\n')
        af.write('题号    ' + '答案' + '\n')
        for ans, content in zip(ans_set, expr_set):
            index += 1
            ef.write(str(index) + '.  ' + content + '\n')
            af.write("{:<5d}".format(index) + '    ' + str(ans) + '\n')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="四则运算")
    parser.add_argument('-n', dest='number', type=int, default=1000, help='生成题目的个数')
    parser.add_argument('-r', dest='range', type=int, default=10, help='数字范围')
    parser.add_argument('-e', dest='exercise', type=str, help='给定题目文件')
    parser.add_argument('-a', dest='answer', type=str, help='给定答案文件')
    parser.add_argument('-g', dest='grade', type=str, help='输出答案文件')
    args = parser.parse_args()

    if args.range is None:
        print("必须输入 -r 限制题目中数值范围")
        exit()
    if args.number is None:
        print("必须输入 -n 选择输出题目数量")
        exit()

    if args.exercise is None:
        args.exercise = os.path.join(os.getcwd(), 'Exercises.txt')
    if args.answer is None:
        args.answer = os.path.join(os.getcwd(), 'Answer.txt')
    if args.grade is None:
        args.grade = os.path.join(os.getcwd(), 'Grade.txt')
    print("答题模式('exit'退出)")

    t = cal.tree()
    u_answer = list()
    formula, s_answer = t.gen_formula(args.range, args.number)
    write_file(formula, s_answer, args.exercise, args.answer)
    for i in range(args.number):
        print(formula[i], end='')
        answer = input()
        if answer == 'exit':
            sys.exit()
        u_answer.append(answer)

    correct, wrong = cal.Cal.grad(u_answer, s_answer)
    print("答题结果：")
    print('正确题号：', correct)
    print('错误题号：', wrong)

    with open(args.grade, 'w+', encoding='utf-8') as f:
        f.write("{:<9}".format("Correct:") + str(len(correct)) + str(correct) + '\n')
        f.write("{:<9}".format("Wrong:") + str(len(wrong)) + str(wrong) + '\n')
