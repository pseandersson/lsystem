"""
// ================================== \\
  Copyright (C) 2017 Patrik Andersson
          All rights reserved
\\=================================== //
"""
NUMS = set('0123456789.')
MATH_OP = set('+-*/^v')
VARIABLES = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')\
                .difference(MATH_OP).difference('e')

# Brython does not support the float.__eq__(a,b) nor
#  float.__ne__(a,b) yet therefor we have to do
# wrap it to the global scope which then could
# be used in the rules

__EQ__ = float.__eq__
__NE__ = float.__ne__

def Brython__EQ__(a, b):
    """Wrapper method for float.__eq__(a, b)
    for Brython"""
    return a == b

def Brython__NE__(a, b):
    """Wrapper method for float.__ne__(a, b)
    for Brython"""
    return a != b

try:
    import browser
    if browser:
        __EQ__ = Brython__EQ__
        __NE__ = Brython__NE__
except:
    pass

# Below follows proper code

class Operator:
    """Base class for operators"""
    def __init__(self, lhs, rhs, opr):
        self.lhs = lhs
        self.rhs = rhs
        self.opr = opr

    def __str__(self):
        return '(' + str(self.lhs) + ' ' + self.opr + ' ' + str(self.rhs) + ')'

    def __call__(self, **kwargs):
        """Take some input arguments and return a result"""
        rhs = self.rhs
        lhs = self.lhs

        if isinstance(rhs, str):
            rhs = kwargs[rhs]
        if isinstance(rhs, (Operator, Expression)):
            rhs = rhs(**kwargs)

        if isinstance(lhs, str):
            lhs = kwargs[lhs]
        if isinstance(lhs, (Operator, Expression)):
            lhs = lhs(**kwargs)

        return self.opr(lhs, rhs)


def calculate(instr):
    """Global functions to resolve mathematical expression
    such as: 2((5e-1-2)+1)/3+2*(4)"""
    instr += ' '  # Add end padding to simplify algo
    mem_val = None
    mem_val_base = None
    rvalue = 0.0
    last_op = ''
    val_str = ''
    bracket_start = None
    bracket_val = None
    bracket_count = 0

    i = 0
    _len = len(instr)
    while i < _len:
        lvalue = None
        cur_op = None

        # check if we are not in a bracket
        # context
        if bracket_count is 0:
             # Store operatator
            if instr[i] in MATH_OP:
                cur_op = instr[i]
            # Add numerical value to the
            # value string
            if instr[i] in NUMS:
                val_str += instr[i]
            # if a minus sign present and
            # value string is empty use it
            # as a sign indicator
            elif instr[i] == '-' and \
                    (val_str == '' or val_str[-1] == 'e')\
                     and bracket_val is None:
                lvalue = -1.0
                cur_op = '*'

                if val_str and val_str[-1] is 'e':
                    val_str += instr[i]
                    lvalue = 1.0
            elif instr[i] == 'e' and \
                    val_str != '' and\
                    val_str[-1] != '-':
                val_str += instr[i]
            # Otherwise try to resolve the value
            else:
                # Let it through ValueError
                # on failure since then the
                # formula contains variables
                if val_str:
                    lvalue = float(val_str)
                    val_str = ''
                # bracket values are returned in the
                # next loop of the string so it has
                # correspondance to an operator
                elif bracket_val != None:
                    lvalue = bracket_val
                    bracket_val = None

                # If a bracket context is
                # at beginning, enable lazy brackets
                # so it is possible to write
                # 2(3-1) = 4
                if instr[i] is '(':
                    if lvalue is not None and cur_op is None:
                        cur_op = '*'
                    bracket_count += 1
                    bracket_start = i + 1
        else:
            # end bracket context
            if instr[i] is ')':
                bracket_count -= 1
                if bracket_count is 0:
                    bracket_val =\
                        calculate(instr[bracket_start:i])
            elif instr[i] is '(':
                bracket_count += 1
            i += 1
            continue

        if mem_val_base != None and lvalue != None:
            lvalue = pow(mem_val_base, lvalue)
            mem_val_base = None

        # Do math operations
        if lvalue is not None:
            if mem_val is None:
                mem_val = lvalue
            else:
                if cur_op == '^':
                    mem_val_base = lvalue
                    cur_op = last_op
                elif last_op is '+':
                    rvalue += mem_val
                    mem_val = lvalue
                elif last_op == '-':
                    rvalue += mem_val
                    mem_val = -lvalue
                elif last_op is '*':
                    mem_val *= lvalue
                elif last_op is '/':
                    mem_val /= lvalue
                elif last_op == '^':
                    mem_val = pow(mem_val, lvalue)
                elif last_op == "v":
                    mem_val = min(mem_val, lvalue)

        if cur_op != None:
            last_op = cur_op
        i += 1
    if mem_val != None:
        rvalue += mem_val
    return rvalue


class Expression:
    """Class to evaluate a generic expression"""
    def __init__(self, expr):
        self.__operator = self.__derive(expr)

    def __str__(self):
        return str(self.__operator)

    def is_constant(self):
        """Returns true if the operator is a constant
           expression
        """
        return isinstance(self.__operator, float)

    def __call__(self, **kwargs):
        """Evaluate the expression"""
        if self.is_constant():
            return self.__operator
        return self.__operator(**kwargs)

    def __derive(self, instr):
        """Global functions to resolve mathematical expression
        such as: 2((5e-1-2)+1)/3+2*(4)"""
        instr += ' '  # Add end padding to simplify algo
        mem_val = None
        mem_val_base = None
        rvalue = 0.0
        last_op = ''
        val_str = ''
        bracket_start = None
        bracket_val = None
        bracket_count = 0

        i = 0
        _len = len(instr)
        while i < _len:
            lvalue = None
            cur_op = None

            # check if we are not in a bracket
            # context
            if bracket_count is 0:
                # Store operatator
                if instr[i] in MATH_OP:
                    cur_op = instr[i]
                # Add numerical value to the
                # value string
                if instr[i] in NUMS:
                    val_str += instr[i]
                # if a minus sign present and
                # value string is empty use it
                # as a sign indicator
                elif instr[i] == '-' and \
                        (val_str == '' or val_str[-1] == 'e')\
                        and bracket_val is None:
                    lvalue = -1.0
                    cur_op = '*'

                    if val_str and val_str[-1] is 'e':
                        val_str += instr[i]
                        lvalue = 1.0
                elif instr[i] == 'e' and \
                        val_str != '' and\
                        val_str[-1] != '-':
                    val_str += instr[i]
                # Capture the variable name
                elif instr[i] in VARIABLES and not val_str:
                    val_str += instr[i]
                # Otherwise try to resolve the value
                else:
                    if val_str:
                        try:
                            lvalue = float(val_str)
                        except ValueError:
                            lvalue = val_str
                        val_str = ''

                    # bracket values are returned in the
                    # next loop of the string so it has
                    # correspondance to an operator
                    elif bracket_val != None:
                        lvalue = bracket_val
                        bracket_val = None

                    # If a bracket context is
                    # at beginning, enable lazy brackets
                    # so it is possible to write
                    # 2(3-1) = 4
                    if instr[i] is '(':
                        if lvalue is not None and cur_op is None:
                            cur_op = '*'
                        bracket_count += 1
                        bracket_start = i + 1
            else:
                # end bracket context
                if instr[i] is ')':
                    bracket_count -= 1
                    if bracket_count is 0:
                        bracket_val =\
                            self.__derive(instr[bracket_start:i])
                elif instr[i] is '(':
                    bracket_count += 1
                i += 1
                continue

            if mem_val_base != None and lvalue != None:
                if isinstance(lvalue, float) and\
                    isinstance(mem_val_base, float):
                    lvalue = pow(mem_val_base, lvalue)
                else:
                    lvalue = Operator(mem_val_base, lvalue, pow)
                mem_val_base = None

            # Do math operations
            if lvalue is not None:
                if mem_val is None:
                    mem_val = lvalue
                elif isinstance(lvalue, float) and\
                     isinstance(mem_val, float) and\
                     isinstance(rvalue, float):
                    if cur_op == '^':
                        mem_val_base = lvalue
                        cur_op = last_op
                    elif last_op is '+':
                        rvalue += mem_val
                        mem_val = lvalue
                    elif last_op == '-':
                        rvalue += mem_val
                        mem_val = -lvalue
                    elif last_op is '*':
                        mem_val *= lvalue
                    elif last_op is '/':
                        mem_val /= lvalue
                    elif last_op == '^':
                        mem_val = pow(mem_val, lvalue)
                    elif last_op == "v":
                        mem_val = min(mem_val, lvalue)
                else:
                    if cur_op == '^':
                        mem_val_base = lvalue
                        cur_op = last_op
                    elif last_op is '+':
                        rvalue = Operator(rvalue, mem_val, float.__add__)
                        mem_val = lvalue
                    elif last_op == '-':
                        rvalue = Operator(rvalue, mem_val, float.__add__)
                        mem_val = -lvalue
                    elif last_op is '*':
                        mem_val = Operator(mem_val, lvalue, float.__mul__)
                    elif last_op is '/':
                        mem_val = Operator(mem_val, lvalue, float.__truediv__)
                    elif last_op == '^':
                        mem_val = Operator(mem_val, lvalue, pow)
                    elif last_op == "v":
                        mem_val = Operator(mem_val, lvalue, min)

            if cur_op != None:
                last_op = cur_op
            i += 1
        if mem_val != None:
            if isinstance(mem_val, float) and isinstance(rvalue, float):
                return rvalue + mem_val
            else:
                return Operator(rvalue, mem_val, float.__add__)
        return rvalue
