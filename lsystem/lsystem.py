"""
// ================================== \\
  Copyright (C) 2016 Patrik Andersson
          All rights reserved
\\=================================== //
"""

from random import random as rand

from lsystem.lmath import calculate, Expression

class LNode(object):
    """LNode is a node in a tree graph representing one command in the Liedermayer system.
       The LNode knows its position in the tree, so it is possible to navigate up() and down()
       in the branch belonging to the nodes.
       LNode also knows its position in the string, so it is possible to know its next()
       command and its previous command with the command prev().
       In order to compare rules against commands in the string a tree matching functionality
       is implemented into the node via the function match(). The logic respects context as
       branches."""

    def __init__(self, val='', predecessor=None):
        self.childs = []
        self.predecessor = predecessor
        self.descendants = 0
        self.depth = -1
        self.val = val
        self.arguments = []
        # self.update_max_depth(1)

    def __eq__(self, b):
        if isinstance(b, str):
            return self.val == b
        elif isinstance(b, LNode):
            return id(self) == id(b)
        else:
            return False

    def get_predecessor(self):
        """Get the parent node"""
        return self.predecessor

    def set_arguments(self, args, to_expression=True):
        """set_arguments of node"""
        if isinstance(args, str):
            if to_expression:
                self.arguments = [Expression(arg) for arg in args[1:-1].split(',')]
            else:
                self.arguments = args[1:-1].split(',')
        elif isinstance(args, (list, tuple)):
            self.arguments = args

    def has_arguments(self):
        """Evaluate if node has any arguments"""
        return bool(self.arguments)

    def get_argument(self, index):
        """get_argument at position index"""
        return self.arguments[index]

    def get_argument_count(self):
        """Returns number of available arguments"""
        return len(self.arguments)

    def get_arguments(self):
        """Returns all arguments of node"""
        return self.arguments

    def update_max_depth(self, depth):
        """Update the depth for the nodes predecessor"""
        self.depth = max(self.depth, depth)  # cannot decresease depth suddenly
        if not self.is_root() and not self.is_branch():
            try:
                self.predecessor.update_max_depth(self.depth + 1)
            except RuntimeError:
                pass

    def increase_descendants(self):
        """Deprecated. Keep control of how many descendants
        there are for the LNode"""
        self.descendants += 1
        if not self.is_root():
            self.predecessor.increase_descendants()

    def add_branch(self, val):
        """Deprecated. see add_child() instead"""
        self.childs.append(LNode(val, self))
        # self.increase_descendants()
        return self.childs[-1]

    def get_childs(self):
        """Access all childrens"""
        return self.childs

    def add_child(self, val, *args, **kwargs):
        """Add a new command val as child to current node"""
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

    def is_branch(self):
        """Check whether current node is a branch node or not"""
        return self.val in '[]'

    def is_child(self):
        """Check if current node is a child node or not"""
        return not self.is_branch() and not self.is_root()

    def is_root(self):
        """Check if current node is root or not"""
        return self.predecessor is None

    def up(self):
        """Navigate upwards in the tree structure."""
        if self.is_root():
            raise StopIteration
        else:
            if self.predecessor.val == '[':
                return self.predecessor.up()
            else:
                return self.predecessor

    def down(self, last_child=None):
        """Navigate downwards in the tree.
        If last_child is given, it will go down
        in the sibling node to last_child which is
        ordered after last_child in childs. If
        last_child is last item, StopIteration is raised"""

        if len(self.childs) == 0:
            raise StopIteration
        else:
            if last_child != None:
                i = self.childs.index(last_child)
                if i + 1 < len(self.childs):
                    return self.childs[i + 1]
                else:
                    raise StopIteration
            else:
                return self.childs[0]


    def has_childs(self):
        """Check wheter the node has childs or not"""
        return bool(self.childs)

    def last_child(self):
        """Internal function for prev()"""
        if self.has_childs():
            return self.childs[-1].last_child()
        else:
            return self

    def prev(self, last_child=None):
        """Go to the previous node in the string-space"""
        if last_child is None:
            if self.is_root():
                raise StopIteration
            else:
                return self.predecessor.prev(self)
        else:
            i = self.childs.index(last_child)
            if i - 1 < 0:
                return self
            else:
                return self.childs[i - 1].last_child()

    def next_at_parent(self):
        """Internal function for next()"""
        try:
            if not self.is_root():
                return self.predecessor.next(self)
            else:
                raise StopIteration
        except RuntimeError:
            raise StopIteration


    def next(self, last_child=None):
        """Deprecated. Use Iterator instead Go to next function in the string-space"""
        if len(self.childs) == 0:
            return self.next_at_parent()
        else:
            if last_child is None and self.has_childs():
                return self.childs[0]
            else:
                i = self.childs.index(last_child)

                if i + 1 < len(self.childs):
                    return self.childs[i + 1]
                else:
                    return self.next_at_parent()


    def to_string(self, traverse=False, newline=False, indent=1, print_args=True):
        """Returns the string, building up the node-scheme"""
        tstr = self.val
        if self.has_arguments() and print_args:
            tstr += '('
            for i in range(0, self.get_argument_count()):
                tstr += str(self.get_argument(i))
                if i < self.get_argument_count() - 1:
                    tstr += ','
                else:
                    tstr += ')'
        if traverse:
            if newline:
                for node in self.childs:
                    tstr += '\n' +  ' '*indent + str(node.to_string(traverse, newline, indent+1, print_args))
            else:
                for node in self.childs:
                    tstr += str(node.to_string(traverse, newline, indent, print_args))
        return tstr


    def print_tree(self, indent=0):
        """Print the node tree to a text string"""
        ostr = str().zfill(indent).replace('0', ' ') + self.val
        ostr += " (" + str(self.depth) + ")"
        print(ostr)
        for node in self.childs:
            node.print_tree(indent + 2)

class LNodeIterator(object):
    """An iterator class to loop over LNodeItems"""
    def __init__(self, first_node: LNode):
        self.node = None
        self.child_iter = [iter([first_node])]

    def __iter__(self):
        return self

    def __next__(self):
        """Go to next function in the string-space"""
        while self.child_iter:
            for self.node in self.child_iter[-1]:
                self.child_iter.append(iter(self.node.get_childs()))
                return self.node

            self.child_iter.pop()

        # This code is to force the iterator to continue if
        # the initial item is in the middle of the tree.
        while not self.node.is_root():
            itr = iter(self.node.predecessor.get_childs())
            is_last = False
            for node in itr:
                if is_last:
                    is_last = False
                    self.node = node
                    break
                if node is self.node:
                    is_last = True
                    self.child_iter.append(itr)
                    self.node = self.node.predecessor

            if not is_last:
                for self.node in self.child_iter[-1]:
                    self.child_iter.append(iter(self.node.get_childs()))
                return self.node

        raise StopIteration

        # TODO might be necessary to check if it's root
        # and work the way up

class LNodeUpIterator(object):
    """Class to iterate backwards"""
    def __init__(self, first_node: LNode, ignore: set, max_depth=-1, ):
        self.node = first_node
        self.max_depth = max_depth
        self.ignore = ignore

    def __iter__(self):
        return self

    def __next__(self):
        self.node = self.node.predecessor
        while self.node is not None and self.node.val in self.ignore:
            self.node = self.node.predecessor

        if self.node is None or self.max_depth is 0:
            raise StopIteration
        self.max_depth -= 1
        return self.node

class LNodeInsertIterator:
    """An iterator class which enabling insert a copy or copy
       an other node(s) or node-tree into a new or existing tree.
       At each iteration, one can customize each individually
       e.g. applying arguments expressions.

       After iterating through the nodes one can access the
       beginning of the new node with get_begin_node() also
       the last node can be accessed with get_end_node()
    """
    def __init__(self, source, target=None, limit=-1, **kwargs):
        self.first_child = False
        self.first = target or LNode()
        self.child_iters = [iter([source])]
        self.nodes = [self.first]
        self.node = self.first
        self.limit = limit
        self.kwargs = kwargs

    def set_limit(self, limit):
        """Restrict the iterator to only insert
           limit number of nodes in the new graph"""
        self.limit = limit

    def set_kwargs(self, **kwargs):
        """Defining the variables for"""
        self.kwargs = kwargs

    def set_target(self, target=None):
        """Set a target so it could be iterating through
           in another place"""
        self.first_child = True
        self.first = target or LNode()
        self.nodes = [self.first]
        self.node = self.first

    def get_begin_node(self):
        """Access the first newly added node"""
        if self.first_child and self.first.get_childs():
            return self.first.get_childs()[-1]
        else:
            return self.first

    def get_end_node(self):
        """Access the end-point where new nodes could be append to"""
        return self.node

    def __iter__(self):
        return self

    def __next__(self):
        while self.child_iters and self.limit:
            child_iter = self.child_iters[-1]
            for node in child_iter:
                if node.get_childs():
                    self.child_iters.append(iter(node.get_childs()))
                if node.val is '':
                    self.nodes.append(self.node)
                else:
                    self.node = self.nodes[-1].add_child(node.val, *node.arguments, **self.kwargs)
                    if node.get_childs():
                        self.nodes.append(self.node)
                    if self.limit > 0:
                        self.limit -= 1
                    return self.node, node
            if child_iter is self.child_iters[-1]:
                self.child_iters.pop()
                self.nodes.pop()

        # Make sure, iff possible, remove the first empty value
        if self.first.val is '' and len(self.first.get_childs()) is 1:
            self.first = self.first.get_childs()[0]

        # Make sure that we end up, before any branches starts
        # or as high up as possible
        if self.node.val is ']' and self.node.predecessor:
            branch_count = 1
            self.node = self.node.predecessor
            while branch_count > 0 and self.node.predecessor:
                if self.node.val is '[':
                    branch_count -= 1
                elif self.node.val is ']':
                    branch_count += 1
                self.node = self.node.predecessor

        raise StopIteration

class LTree(object):
    """LTree is a class to organize L-System instructions into LNode's.
    After the tree has been created one can access the nodes by chop()
    function. The chop()-function gives access to the nodes and remove
    their relationship to LTree so new trees can grow up there"""

    def __init__(self, initstr=None, parse_args=True):
        self.states = []
        self.root = LNode()
        self.node = self.root
        self.parse_args = parse_args
        self.n_fetch_nodes = -1

        if isinstance(initstr, str):
            self.push(initstr)

    def __lshift__(self, instr):
        """Push strings or nodes into the tree structure"""
        if isinstance(instr, str):
            self.push(instr)
        elif isinstance(instr, int):
            self.n_fetch_nodes = instr
        elif isinstance(instr, LNodeInsertIterator):
            instr.set_target(self.node)
            for i in instr:
                pass
            self.node = instr.get_end_node()
        elif isinstance(instr, LNode):
            itr = LNodeInsertIterator(instr, self.node, self.n_fetch_nodes)
            for a in itr:
                pass
            self.node = itr.get_end_node()
            self.n_fetch_nodes = -1
        return self

    def chop(self, **args):
        """Chopping trees to get access to its stems, branches and leaves,
         so new tree can be planted and grow"""
        if 'make_depth' in args.keys():
            node = self.root
            while args['make_depth']:
                node.update_max_depth(1)
                try:
                    node = node.next()
                except StopIteration:
                    break
        tree = None
        if len(self.root.childs) == 1:
            tree = self.root.childs.pop()
            tree.predecessor = None
        else:
            tree = self.root
        self.root = LNode()
        self.node = self.root
        self.states = []
        return tree

    def first(self):
        tree = None
        if len(self.root.childs) == 1:
            tree = self.root.childs[0]
            tree.predecessor = None
        else:
            tree = self.root
        return tree

    def push(self, instr):
        """Push back literals to construct the tree"""
        slen = len(instr)
        i = 0
        bracket_start_pos = None
        bracket_count = 0

        while i < slen:
            if instr[i] == '(':
                bracket_start_pos = i
                bracket_count += 1
                i += 1
                while i < slen:
                    if instr[i] == '(':
                        bracket_count += 1
                    elif instr[i] == ')':
                        bracket_count -= 1
                    if bracket_count == 0:
                        break
                    i += 1
                self.node.set_arguments(instr[bracket_start_pos:i + 1], self.parse_args)
            elif instr[i] == '[':
                self.states.append(self.node)
                self.node = self.node.add_child(instr[i])
                # new_branch = True
            elif instr[i] == ']':
                self.node = self.node.add_child(instr[i])
                self.node = self.states.pop()
            else:
                key = instr[i]
                if i + 1 < slen:
                    if instr[i + 1] == '_':
                        key += instr[i + 1:i + 3]
                        i += 2

                self.node = self.node.add_child(key)

            i += 1


    def print_tree(self):
        """Display the tree"""
        if len(self.root.childs) == 1:
            self.root.childs[0].print_tree()
        else:
            self.root.print_tree()

    def to_string(self):
        s = ''
        for node in LNodeIterator(self.root):
            s += node.to_string()
        return s

class LRule(object):
    """Class to handle rules and logics"""
    DETERMINISTIC_RULE = 0
    STOCHASTIC_RULE = (1 << 0)

    SUBSCRIPT = (1 << 0)
    LOOK_BEFORE = (1 << 1)
    LOOK_AFTER = (1 << 2)
    BRACKETS = (1 << 3)
    BRACKET_ERROR = (1 << 4)
    FUNC_DEF = (1 << 5)

    def __init__(self, initstr, consequences, ignore: set=None):
        self.flag = 0
        self.key = None
        self.less = None
        self.greater = None
        self.consequences = None
        self.prob_rules = []
        self.cs = None  # Cummulative Sum
        self.functions = []
        self.expressions = []
        self.cmp_type = None
        self.fn_str = None
        self.cmp_str = None
        self.ignore = ignore or set()
        self.type = self.DETERMINISTIC_RULE

        self.setup_case(initstr)
        self.setup_consequences(consequences)

    def setup_case(self, initstr):
        """Setup the instructions for the trial case"""
        i = 0
        less_pos = None
        great_pos = None
        bracket_count = 0
        commas = []
        while i < len(initstr):
            if initstr[i] == '<':
                self.flag |= self.LOOK_BEFORE
                less_pos = i + 1
            elif initstr[i] == '>':
                self.flag |= self.LOOK_AFTER
                great_pos = i
            elif initstr[i] == '(':
                self.flag |= self.BRACKETS
                self.flag |= self.BRACKET_ERROR
                bracket_count += 1
            elif initstr[i] == ')':
                self.flag &= ~self.BRACKET_ERROR
                bracket_count -= 1
            elif initstr[i] == ':':
                self.flag |= self.FUNC_DEF
                break
            elif initstr[i] == ',':
                commas.append(i)
            i += 1

        key_string = None

        if self.flag & self.FUNC_DEF:
            key_string = initstr[0:i]
        else:
            key_string = initstr
        # TODO Assumes only one function e.g. F(x,t)
        # in future multiple keys should be supported
        # e.g. F(x,t)G(y,t)
        self.key = (LTree('', False) << key_string[less_pos:great_pos]).chop()

        if self.flag & self.LOOK_BEFORE:
            self.less = (LTree() << key_string[0:less_pos - 1]).chop(make_depth=True)

        if self.flag & self.LOOK_AFTER:
            self.greater = (LTree() << key_string[great_pos + 1:]).chop()

        if self.flag & self.FUNC_DEF:
            self.setup_func(initstr[(i + 1):])

    def setup_func(self, funcstr):
        """Set up the functions using during comparison"""
        funcstrs = funcstr.split('&&')
        ### TODO Expand Expresssions to handle all this
        for fnstr in funcstrs:
            cmp_type = '', None
            if '<=' in funcstr:
                cmp_type = '<=', float.__le__
            elif '>=' in funcstr:
                cmp_type = '>=', float.__ge__
            elif '==' in funcstr:
                cmp_type = '==', float.__eq__
            elif '!=' in funcstr:
                cmp_type = '!=', float.__ne__
            elif '<' in funcstr:
                cmp_type = '<', float.__lt__
            elif '>' in funcstr:
                cmp_type = '>', float.__gt__

            pos = fnstr.find(cmp_type[0])
            fn_str = funcstr[0:pos]
            cmp_str = funcstr[pos + len(cmp_type[0]):]
            self.functions.append((Expression(fn_str), Expression(cmp_str), cmp_type[1]))

    def add_consequence(self, consequence):
        """Add a consequence and prepare all expressions"""
        self.prob_rules.append((LTree(consequence)).chop())

    def setup_consequences(self, consequences):
        """Setup the consequences"""
        if isinstance(consequences, dict):
            self.type = self.STOCHASTIC_RULE
            itr = iter(consequences)

            self.cs = [0.]
            try:
                while True:
                    rule = itr.next()
                    prob = consequences[rule]
                    self.cs.append(prob + self.cs[-1])
                    self.add_consequence(rule)
            except StopIteration:
                pass
            self.cs[:] = [x / self.cs[-1] for x in self.cs]

        else:
            self.add_consequence(consequences)

    def trial(self, node):
        """Test if the node follows the rule. Returns True if it does,
        otherwise False."""
        bf_node = None
        af_node = None

        if not self.simple_rule_match(self.key, node):
            return False, None
        # print 'Key', self.key.val
        if self.flag & self.LOOK_BEFORE:
            lnode = node
            try:
                for i in range(self.less.depth):
                    lnode = lnode.up()
                    while lnode.val in self.ignore:
                        lnode = lnode.up()

                if not self.match(lnode, self.less):
                    return False, None
                else:
                    bf_node = lnode
            except StopIteration:
                return False, None

        if self.flag & self.LOOK_AFTER:
            try:
                if self.match(node.next(), self.greater):
                    af_node = node.next()
                else:
                    return False, None
            except StopIteration:
                return False, None

        # Create argument list
        arglist = dict(zip(self.key.get_arguments(), node.get_arguments()))

        if bf_node:
            self.match(bf_node, self.less, arglist)
        if af_node:
            self.match(af_node, self.greater, arglist)

        state = True

        # Evaluate function
        if self.flag & self.FUNC_DEF:
            # Might be useful in the future
            # if self.key.get_argument_count()!=\
            #	node.get_argument_count():
            #	return False
            for fn_str, cmp_str, cmp_opr in self.functions:
                state = cmp_opr(fn_str(**arglist), cmp_str(**arglist))

                if not state:
                    break

        return state, arglist

    def return_rule(self, arglist: dict=None, rule_id=1):
        """Returning aCopy the protype with applyied
           argumentlist return"""
        return LNodeInsertIterator(self.prob_rules[rule_id -1], **(arglist or {}))
        # for n in new_rule_itr:
        #     pass

        # return new_rule_itr.get_begin_node()


    def try_case(self, case_str):
        """Test if the string follows the given rule, if it does
        then it returns the replacement string otherwise None."""
        success, arglist = self.trial(case_str)
        if success:
            if self.cs is None:
                return self.return_rule(arglist)
            else:
                r = rand()
                for k in range(0, len(self.cs)):
                    if r < self.cs[k]:
                        return self.return_rule(arglist, k)
        else:
            return None

    def simple_rule_match(self, a, b):
        if a.val == b.val:
            if a.get_argument_count() == b.get_argument_count():
                return True
        return False

    def parse_arguments(self, a, b, d):
        """Internal method to parse arguments"""
        for i in range(0, a.get_argument_count()):
            if not a.get_argument(i) in d.keys():
                d[a.get_argument(i)] = float(b.get_argument(i))
            else:
                print('Argument error')


    def match(self, a, b, arglist=None):
        """Compare two different LNode-system to see if they match.
        a is the instruction b is the rule."""
        if type(a) == type(b):
            # print a.val,'==',b.val
            if self.simple_rule_match(a, b):
                if isinstance(arglist, dict):
                    self.parse_arguments(a, b, arglist)
                if a.has_childs() and b.has_childs():
                    cmp_child = True
                    i = 0
                    j = 0
                    while i < len(a.childs) and j < len(b.childs):
                        cmp_child = self.match(
                            a.childs[i], b.childs[j], arglist)

                        if not cmp_child:
                            if a.childs[i].val == '[':
                                j -= 1
                            else:
                                return False
                        i += 1
                        j += 1

                    return bool(i == len(b.childs))
                elif a.has_childs() and not b.has_childs():
                    return True
                elif not a.has_childs() and b.has_childs():
                    return False
                else:
                    return True
            elif b.val == '*':
                return True
            elif a.val in self.ignore:
                try:
                    return self.match(a.next(), b, arglist)
                except StopIteration:
                    return False
            elif b.val == ']':
                return True
            elif a.val == '[':
                is_ok = False
                try:
                    node = a.up().down(a)
                    is_ok = self.match(node, b, arglist)
                except StopIteration:
                    return False
                return is_ok
            else:
                return False
        elif isinstance(b, str):
            #			print 'TXT:',self.val,'==',b
            return bool(a.val == b and not a.has_childs())
        else:
            return False

class LSystem(object):
    """Builder pattern to create a tree"""
    def __init__(self):
        self.rules = []
        self.rules_dict = {}
        self.nmax = -1
        self.itree = LTree()
        self.figures = []
        self.definitions = {}
        self.ignore = set()

    def set_figures(self, figures: dict):
        """Set figures, e.g.  figures = {'L':'','R':''}"""
        for law, conseq in figures.items():
            self.figures.append(LRule(law, conseq))
        return self

    def set_ignore(self, ignore: str):
        """Ignore certain syntax, e.g. ignore = '+-F'"""
        self.ignore = set(ignore)
        return self

    def set_definitions(self, definitions: dict):
        """Define variables to be used in the rules, e.g.
        define = {
            'c':'1',
            'p':'0.3',
            'q':'c-p',
            'h':'(p*q)^0.5'
        }
        rules ={
            'F(x,t):t==0':'F(x*p,2)+F(x*h,1)--F(x*h,1)+F(x*q,0)',
            'F(x,t):t>0':'F(x,t-1)'
        }
        """
        if isinstance(definitions, dict):
            self.definitions = definitions.copy()
        return self

    def __resolve_definitions(self):
        """
            Resolve all definitions
        """
        changes_made = True
        while changes_made:
            changes_made = False
            for key, value in self.definitions.items():
                # replace all expressions such that only
                # numeric items are remaining
                for _key, _value in self.definitions.items():
                    tmp_val = value
                    value = value.replace(_key, '(' + _value + ')')
                    if not tmp_val == value:
                        changes_made = True
                    self.definitions[key] = value
        # Compute the defintions values
        for key, value in self.definitions.items():
            self.definitions[key] = str(calculate(value))


    def __resolve_rules(self):
        for law, conseq in self.rules_dict.items():
            # Resolve all predefined variables
            if self.definitions:
                for key, value in self.definitions.items():
                    conseq = conseq.replace(key + '(', value + '*')
                    conseq = conseq.replace(key, value)
                print('conseq', conseq)
            self.rules.append(LRule(law, conseq, self.ignore))

    def set_rules(self, rules):
        """Set rules for the lsystem e.g

        rules ={
            'F(x,t):t==0':'F(x*p,2)+F(x*h,1)--F(x*h,1)+F(x*q,0)',
            'F(x,t):t>0':'F(x,t-1)'
        }

        """
        self.rules_dict = rules
        return self

    def set_max_iterations(self, max_iterations: int):
        """Set maximum iterations for the L-System"""
        self.nmax = max_iterations
        return self

    def __solve(self, rules):
        """Private method solve the L-System for one iteration
              rules     - could be self.rules or the self.figures
        """
        node = self.itree.chop()
        itr = LNodeIterator(node)
        for node in itr:
            new_str = None

            for rule in rules:
                new_str = rule.try_case(node)
                if new_str:
                    self.itree << new_str
                    break

            if not new_str:
                n = LNode(node.val)
                n.set_arguments(node.get_arguments())
                self.itree << 1 << n

    def solve(self, instr):
        if isinstance(instr, str):
            self.itree << instr
        elif isinstance(instr, LTree):
            self.itree = instr
        else:
            raise RuntimeError

        # Make sure that definitions are
        # resolved before the rules
        self.__resolve_definitions()
        self.__resolve_rules()

        for n in range(self.nmax):
            print('Iteration:', n)
            self.__solve(self.rules)
        if self.figures:
            self.__solve(self.figures)
        return self.itree
