from mip import *


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def split_vars(var):
    var = var + '+'
    out_var: list = []
    keep_last = 0

    for ii in range(len(var)):
        if var[ii].isalpha():

            if keep_last == ii == 0:
                out_var.append(1)
            elif var[keep_last: ii] == '+' or var[keep_last: ii] == '-':
                out_var.append(1)
            else:
                out_var.append(int(var[keep_last: ii]))
            keep_last -= keep_last
            keep_last += ii

        elif var[ii] == '+' or var[ii] == '-':
            out_var.append(var[keep_last: ii])
            keep_last -= keep_last
            keep_last += ii

    return out_var


if __name__ == '__main__':

    # input objective function and optimization sense format
    # and split them
    s = input().split()
    m = Model(sense=s[0].upper(), solver_name=CBC)
    var_list = split_vars(s[1])

    # add variables to model
    x = [m.add_var(name=var_list[(2 * i) + 1]) for i in range(int(len(var_list) / 2))]

    # add objective function
    m.objective = xsum(var_list[2*i] * x[i] for i in range(len(x)))

    # add constraints
    while True:
        s = input()
        if s == 'end':
            break
        s = s.split()
        varies = split_vars(s[0])

        # checking the operator (final phase)
        if s[1] == '=':
            m += xsum(varies[2 * i] * m.var_by_name(varies[(2 * i) + 1]) for i in range(len(x))) == int(s[2])
        elif s[1] == '<=':
            m += xsum(varies[2 * i] * m.var_by_name(varies[(2 * i) + 1]) for i in range(len(x))) <= int(s[2])
        elif s[1] == '>=':
            m += xsum(varies[2 * i] * m.var_by_name(varies[(2 * i) + 1]) for i in range(len(x))) >= int(s[2])

    # Optimize and Print the results
    m.optimize()
    print(Color.RED + Color.BOLD + "\n\t Objective Value =", m.objective_value, Color.END)
    for i in range(len(x)):
        print(Color.BLUE + Color.BOLD + "- {} =".format(m.var_by_name(var_list[2*i + 1])), x[i].x, Color.END)
