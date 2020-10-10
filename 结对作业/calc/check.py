from fractions import Fraction


def get_num_op(formula):
    num_list = list()
    op_list = list()
    for item in formula:
        if isinstance(item, int) or isinstance(item, Fraction):
            num_list.append(item)
        elif item == ' ＋ ':
            op_list.append(item)
        elif item == ' － ':
            op_list.append(item)
        elif item == ' × ':
            op_list.append(item)
        elif item == ' ÷ ':
            op_list.append(item)
    return num_list, op_list


def check(formula, form):
    f_nlist, f_olist = get_num_op(formula)
    if ' ＋ ' in f_olist or ' × ' in f_olist:
        n_list, o_list = get_num_op(form)
        if f_nlist.sort() == n_list.sort():
            return True
    else:
        return False



