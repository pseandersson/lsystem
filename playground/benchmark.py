import random
import bisect
import matplotlib.pyplot as plt
import time
import math
import string
import re
from lsystem import LNode
from lmath import Expression


def method_in(a, b, c):
    start_time = time.time()
    for i, x in enumerate(a):
        if x in b:
            c[i] = 1
    return(time.time() - start_time)


def method_set_in(a, b, c):
    start_time = time.time()
    s = set(b)
    for i, x in enumerate(a):
        if x in s:
            c[i] = 1
    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)


def method_bisect(a, b, c):
    start_time = time.time()
    b.sort()
    for i, x in enumerate(a):
        index = bisect.bisect_left(b, x)
        if index < len(a):
            if x == b[index]:
                c[i] = 1
    return(time.time() - start_time)


def profile():
    time_method_in = []
    time_method_set_in = []
    time_method_bisect = []

    Nls = [x for x in range(1000, 20000, 1000)]
    for N in Nls:
        a = [x for x in range(0, N)]
        random.shuffle(a)
        b = [x for x in range(0, N)]
        random.shuffle(b)
        c = [0 for x in range(0, N)]

        time_method_in.append(math.log(method_in(a, b, c)))
        time_method_set_in.append(math.log(method_set_in(a, b, c)))
        time_method_bisect.append(math.log(method_bisect(a, b, c)))

    plt.plot(Nls, time_method_in, marker='o',
             color='r', linestyle='-', label='in')
    plt.plot(Nls, time_method_set_in, marker='o',
             color='b', linestyle='-', label='set')
    plt.plot(Nls, time_method_bisect, marker='o',
             color='g', linestyle='-', label='bisect')
    plt.xlabel('list size', fontsize=18)
    plt.ylabel('log(time)', fontsize=18)
    plt.legend(loc='upper left')
    plt.show()


def method_in_multi(a, b, c):
    a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12 = a
    start_time = time.time()

    for i, x in enumerate(b):
        for y in a:
            if y in x:
                c[i] = 1
                break
    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)


def method_in_multi_const(a, b, c):
    start_time = time.time()
    for i, x in enumerate(b):
        if ('', '^', 'v', '0(', '1(', '2(', '3(', '4(', '5(', '6(', '7(', '8(', '9(' in x)[-1]:
            c[i] = 1
    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)


def method_regex(a, b, c):
    start_time = time.time()
    for i, x in enumerate(b):
        if a.search(x) is not None:
            c[i] = 1

    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)


def method_set_intersect(a, b, c):
    s = set(a)
    start_time = time.time()
    for i, x in enumerate(b):
        if s.intersection(x):
            c[i] = 1

    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)

def copy_one(a, c, *args, **kwargs):
    start_time = time.time()
    for i in a:
        A = LNode('A')
        c[i] = A.add_child('B').val
    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)

def copy_two(a, c, *args, **kwargs):
    start_time = time.time()
    if args and kwargs:
        for i in a:
            A = LNode('A')
            c[i] = A.add_child2('B', *args, **kwargs).val
    elif args:
        for i in a:
            A = LNode('A')
            c[i] = A.add_child2('B', *args).val
    else:
        for i in a:
            A = LNode('A')
            c[i] = A.add_child2('B').val
    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)

def copy_three(a, c, *args, **kwargs):
    start_time = time.time()
    if args and kwargs:
        for i in a:
            A = LNode('A')
            c[i] = A.add_child3('B', *args, **kwargs).val
    elif args:
        for i in a:
            A = LNode('A')
            c[i] = A.add_child3('B', *args).val
    else:
        for i in a:
            A = LNode('A')
            c[i] = A.add_child3('B').val
    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)

def copy_four(a, c, *args, **kwargs):
    start_time = time.time()

    for i in a:
        A = LNode('A')
        c[i] = A.add_child4('B', args).val

    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)

def copy_five(a, c, *args, **kwargs):
    start_time = time.time()

    for i in a:
        A = LNode('A')
        c[i] = A.add_child5('B', args).val

    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)

def copy_six(a, c, *args, **kwargs):
    start_time = time.time()

    for i in a:
        A = LNode('A')
        c[i] = A.add_child6('B', args, kwargs).val

    elapsed = time.time() - start_time
    return max(elapsed, 0.000000001)
""" Methods under test:
    def add_child(self, val):
        self.childs.append(LNode(val, self))
        # self.increase_descendants()
        return self.childs[-1]


    def add_child2(self, val, *args, **kwargs):
        node = LNode(val, self)
        if args:
            if kwargs:
                for arg in args:
                    if isinstance(arg, Expression):
                        node.arguments.append(arg(**kwargs))
                    else:
                        node.arguments.append(arg)
            else:
                node.set_arguments(args)

        self.childs.append(node)
        return self.childs[-1]

    def add_child3(self, val, *args, **kwargs):
        node = LNode(val, self)
        if args:
            if kwargs:
                for arg in args:
                    node.arguments.append(arg(**kwargs))
            else:
                node.set_arguments(*args)
        self.childs.append(node)
        return self.childs[-1]

    def add_child4(self, val, args):
        self.childs.append(LNode(val, self))
        self.childs[-1].set_arguments(args)
        # self.increase_descendants()
        return self.childs[-1]

    def add_child5(self, val, args):
        node = LNode(val, self)
        node.set_arguments(args)
        # self.increase_descendants()
        self.childs.append(node)
        return self.childs[-1]

    def add_child6(self, val, args, in_var):
        node = LNode(val, self)

        self.set_arguments(args)
        for arg in args:
            if isinstance(arg, Expression):
                self.arguments.append(arg(in_var))
            else:
                self.arguments.append(arg)

        self.childs.append(node)
        return self.childs[-1]
"""
def profile_copy():
    methods = [copy_one, copy_two, copy_three, copy_four, copy_five, copy_six]
    labels = ['one', 'two', 'three', 'four', 'five', 'six']
    colors = 'rbmkgc'
    time_methods = [[[], [], [], [], [], []],
                    [[], [], [], [], [], []],
                    [[], [], [], [], [], []],
                    [[], [], [], [], [], []]]
    Nls = [x for x in range(1000, 40000, 1000)]
    combinations = ['No Args', 'Only Kwargs', 'Only Args', 'Both Kwargs and Args']
    inputs = [([], {}),
              ([], {'q':5}),
              ([1.], {}),
              ([Expression('q^2'), 1.], {'q':5})]
    selection = [0, 1, 2]
    for N in Nls:
        a = range(N)
        for i, (args, kwargs) in enumerate(inputs):
            for j in selection:
                c = ['' for x in range(0, N)]
                time_methods[i][j].append(math.log(methods[j](a, c, *args, **kwargs)))
            # print('i:', i, 'len(time_methods[:])', [len(x) for x in time_methods])
    # print(time_methods)
    for k, header in enumerate(combinations):
        plt.subplot(2, 2, k+1)
        for i in selection:
            plt.plot(Nls, time_methods[k][i], marker='o',
                    color=colors[i], linestyle='-', label=labels[i])

            plt.xlabel('list size', fontsize=18)
            plt.ylabel('log(time)', fontsize=18)
            plt.legend(loc='upper left')
            plt.title(header)
    plt.show()

def profile_multi_in():
    time_method_in_multi = []
    time_method_in_multi_const = []
    time_method_regex = []
    time_method_set_intersect = []

    Nls = [x for x in range(1000, 20000, 1000)]
    K = 9
    a_re = re.compile('(\^|v|\d\()')
    a = ['^', 'v', '0(', '1(', '2(', '3(', '4(', '5(', '6(', '7(', '8(', '9(']

    for N in Nls:
        random.shuffle(a)
        b = [''.join(random.choices(string.digits + '.()+-*/^ev', k=K))
             for x in range(0, N)]
        random.shuffle(b)
        c = [0 for x in range(0, N)]

        time_method_in_multi.append(math.log(method_in_multi(a, b, c)))
        time_method_in_multi_const.append(math.log(method_in_multi_const(a, b, c)))
        time_method_regex.append(math.log(method_regex(a_re, b, c)))
        time_method_set_intersect.append(
            math.log(method_set_intersect(a, b, c)))

    plt.plot(Nls, time_method_in_multi, marker='o',
             color='r', linestyle='-', label='in')
    # plt.plot(Nls, time_method_in_multi_const, marker='x',
    #          color='m', linestyle='-', label='in-const')
    plt.plot(Nls, time_method_regex, marker='o',
             color='b', linestyle='-', label='regex')
    # plt.plot(Nls, time_method_set_intersect, marker='o',
    #          color='g', linestyle='-', label='intersect')
    plt.xlabel('list size', fontsize=18)
    plt.ylabel('log(time)', fontsize=18)
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    # profile_multi_in()
    profile_copy()
