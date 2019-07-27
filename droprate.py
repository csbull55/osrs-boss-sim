# Christian Bull
"""
this holds the gcf, gcf_multi, and lcm functions
includes converting fractions into drop rates
"""


# simple gcf function
def gcf(num_1, num_2):
    a = max(num_1, num_2)
    b = min(num_1, num_2)
    c = 1
    # repeats calc until the remained = 0, returns the value one before that
    while c != 0:
        c = a % b
        a = b
        b = c
        if c == 0:
            gcf_value = a
    return gcf_value


# uses og gcf function to allow for multiple numbers
def gcf_multi(args):
    gcf1 = args[0]
    # takes gcf of first 2 items then for each args[2:]
    for i in args[1:]:
        gcf2 = gcf(gcf1, i)
        i += 1
        gcf1 = gcf2
    return gcf1


# quick function to multiple items of a list to each other
def multi(mylist):
    result = 1
    for i in mylist:
        result = result * i
    return result


def lcm(args):
    return multi(args) / gcf_multi(args)


def lcm_multi(args):
    lcm1 = args[0]
    # takes gcf of first 2 items then for each args[2:]
    for i in args[1:]:
        qlist = [lcm1, i]
        lcm2 = lcm(qlist)
        i += 1
        # lcm is the i index before 0
        lcm1 = lcm2
    return lcm2
