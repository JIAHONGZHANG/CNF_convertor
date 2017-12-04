#!usr/bin/python3
# the convert2CNF function is applied using Python
# this is for COMP4418 at UNSW
# written by Prophet 28/11/2017 and Thanks to Eric Martin who is Dr Eric Matin of COMP9021.
#
# test enviornment:
# Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 17:26:49) [MSCv.1900 32 bit (Intel)] on win32.
# the input format is
#        python convert2CNF.py '[p imp q, (neg r) imp (neg q)] seq [p imp r]'
#
#        imp means    ->
#        neg means    not
#        iff means    <->
#        and means    interception
#        or  means    Union

import argparse
from binarytree import *
from stack import *
import copy

def parserArgument():
    """
    acquire the system parameters
    """
    parser = argparse.ArgumentParser(description = 'Convert2CNF Project')
    parser.add_argument('proposition', type = str,\
        help = "the propsition you need to prove,the format is '(neg r) imp (neg q)'",\
        action = 'store')

    return parser.parse_args()

class CNF(object):
    def __init__(self, proposition):
        self.prop = proposition
        self.prop_list = self.str2list()

    def str2list(self):
        ## this part can relize by using the stack if the C language is used.
        ## but I want to simplify code and improve the efficiency,
        ## so I use some built-in funciton.
        """
        process the text of input.
        """
        # exp_stack = Stack()
        # while 
        prop_list = [i for i in list(self.prop) if i != ' ']
        # new_prop = list()
        for i in range(len(prop_list)):
            if prop_list[i] in ['n', 'a', 'i'] and \
                ''.join(prop_list[i:i+3]) in ['neg', 'and', 'imp', 'iff']:
                prop_list[i:i+3] = [''.join(prop_list[i:i+3]), '', '']
            elif prop_list[i] == 'o' and ''.join(prop_list[i:i+2]) == 'or':
                prop_list[i:i+2] = [''.join(prop_list[i:i+2]), '']
            else:
                pass
        return ['['] + [i for i in prop_list if i != ''] + [']']


    def is_CNF(self):
        """
        check if it satisfy CNF rules.
        """
        pass

    # the De Morgan law:

    def neg_neg(self,BT):
        """
        the neg-neg rules.
        """
        if BT.value == "neg" and BT.left_node.value == "neg":
            BT.value = BT.left_node.left_node.value
            BT.right_node = BT.left_node.left_node.right_node
            BT.left_node = BT.left_node.left_node.left_node
        return BT

    def neg_and_or(self, BT, mode):
        """
        !(p or q) == !p and !q
        !(p and q) == !p or !q
        """
        if BT.value == 'neg' and BT.left_node.value in ['and', 'or']:
            BT.left_node.value = 'neg'
            BT.right_node = BinaryTree("neg")
            if mode == 'neg-or':
                BT.value = 'and'
            elif mode == 'neg-and':
                BT.value = 'or'
            BT.right_node.left_node = BT.left_node.right_node
            BT.left_node.right_node = BinaryTree()
            BT.right_node.right_node = BinaryTree()
        else:
            pass
        return BT


    def or_and(self, BT):
        """
        (p and q) or c = (p or c) and (q or c)
        """ 
        if BT.value == 'or':
            if BT.left_node.value == 'and' and BT.right_node.value != 'and':
                BT.value = "and"
                BT.left_node.value = 'or'
                right_copy_tree = copy.deepcopy(BT.right_node)
                new_tree = BinaryTree("or")
                BT.right_node, new_tree.right_node = new_tree, BT.right_node
                BT.right_node.left_node = BT.left_node.right_node
                BT.left_node.right_node = right_copy_tree

            elif BT.right_node.value == 'and' and BT.left_node.value != 'and':
                BT.value = "and"
                BT.right_node.value = 'or'
                right_copy_tree = copy.deepcopy(BT.left_node)
                new_tree = BinaryTree("or")

                BT.left_node, new_tree.left_node = new_tree, BT.left_node
                BT.left_node.right_node = BT.right_node.left_node
                BT.right_node.left_node = right_copy_tree

            else:
                pass
        else:
            pass

        return BT

    def and_or_and(self, BT):
        """
        (p and q) or (r and t) = (p or r) and (p or t) and (q or r) and (q or t).
        """
        if BT.value == 'or':
            if BT.left_node.value == 'and' and BT.right_node.value == 'and':
                BT.value = 'and'
                new_tree_list = [BinaryTree("or") for _ in range(0,4)]
                new_tree_list[0].left_node = copy.deepcopy(BT.left_node.left_node)
                new_tree_list[0].right_node = copy.deepcopy(BT.right_node.left_node)
                new_tree_list[1].left_node = copy.deepcopy(BT.left_node.left_node)
                new_tree_list[1].right_node = copy.deepcopy(BT.right_node.right_node)
                new_tree_list[2].left_node = copy.deepcopy(BT.left_node.right_node)
                new_tree_list[2].right_node = copy.deepcopy(BT.right_node.left_node)
                new_tree_list[3].left_node = copy.deepcopy(BT.left_node.right_node)
                new_tree_list[3].right_node = copy.deepcopy(BT.right_node.right_node)
    
                BT.left_node.left_node = new_tree_list[0]
                BT.left_node.right_node = new_tree_list[1]
                BT.right_node.left_node = new_tree_list[2]
                BT.right_node.right_node = new_tree_list[3]
            else:
                pass
        else:
            pass
        return BT

    def or_rules(self, BT):
        if BT.value == 'or':
            if BT.left_node.value == 'and' and BT.right_node.value == 'and':
                self.and_or_and(BT)
            else:
                self.or_and(BT)
        else:
            pass
        return BT

    def neg_rules(self, BT):
        """
        find all neg rules and using the law about neg to simplify all the proposition consisiting of neg.
        """
        cur_tree = BT
        stack_for_cal = Stack()
        stack_for_cal.push(cur_tree)
        while not stack_for_cal.is_empty():
            cur_tree = stack_for_cal.pop()
            if cur_tree.value == 'neg':
                if cur_tree.left_node.value == 'neg':
                    self.neg_neg(cur_tree)
                    stack_for_cal.push(cur_tree)
                elif cur_tree.left_node.value in ['or', 'and']:
                    mode = cur_tree.value + '-' + cur_tree.left_node.value
                    self.neg_and_or(cur_tree, mode)
                    stack_for_cal.push(cur_tree.left_node)
                    stack_for_cal.push(cur_tree.right_node)
                else:
                    pass
            else:
                pass

    def imp_rule(self, BT):
        if BT.value == 'imp':
            BT.value = 'or'
            insert_tree = BinaryTree("neg")
            insert_tree.left_node = BT.left_node
            BT.left_node = insert_tree
            self.neg_rules(BT.left_node)
        else:
            pass
        return BT

    def iff_rule(self, BT):
        if BT.value == 'iff':
            BT.value = 'and'
            new_tree = [BinaryTree("imp") for _ in range(2)]
            new_tree[0].left_node = BT.left_node
            new_tree[0].right_node = BT.right_node
            new_tree[1].left_node = copy.deepcopy(BT.right_node)
            new_tree[1].right_node = copy.deepcopy(BT.left_node)
            BT.left_node = new_tree[0]
            BT.right_node = new_tree[1]
            self.imp_rule(BT.left_node)
            self.imp_rule(BT.right_node)
        else:
            pass
        return BT

    def morgan_rules(self, proposition, mode = 'CNF'):
        """
        the converting rules --- De Morgan law.
        """
        rules = {
            'iff': self.iff_rule,
            'imp': self.imp_rule,
            'neg': self.neg_rules,
            'or' : self.or_rules
        }
        if mode == 'CNF':
            rules[proposition.value](proposition)
        elif mode == 'DNF':
            pass
        else:
            pass

    def gen_tries(self, atom_L, root, atom_R):
        """
        generate the binary tries for input proposition.
        """
        if isinstance(atom_L, BinaryTree) is True and isinstance(atom_R, BinaryTree) is True:
            new_tree = BinaryTree(root)
            new_tree.left_node = atom_L
            new_tree.right_node = atom_R
        elif isinstance(atom_L, BinaryTree) is True and isinstance(atom_R, BinaryTree) is False:
            new_tree = BinaryTree(root)
            new_tree.left_node = atom_L
            new_tree.right_node = BinaryTree(atom_R)
        elif isinstance(atom_L, BinaryTree) is False and isinstance(atom_R, BinaryTree) is True:
            new_tree = BinaryTree(root)
            new_tree.left_node = BinaryTree(atom_L)
            new_tree.right_node = atom_R
        else:
            new_tree = BinaryTree(root)
            new_tree.left_node = BinaryTree(atom_L)
            new_tree.right_node = BinaryTree(atom_R)

        return new_tree

    def CNF_simplifier(self):
        """
        simplify the non-CNF proposition. 
        """
        pass

    def showCNF(self):
        """
        showing the CNF result.
        """
        pass





if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    # r = BinaryTree("neg")
    # r.left_node = BinaryTree("neg")
    # r.left_node.left_node = BinaryTree("and")
    # r.left_node.left_node.left_node = BinaryTree("p")
    # r.left_node.left_node.right_node = BinaryTree("q")
    # r.print_binary_tree()

    # r = BinaryTree("neg")
    # r.left_node = BinaryTree("and")
    # r.left_node.left_node = BinaryTree("p")
    # r.left_node.right_node = BinaryTree("q")
    # r.print_binary_tree()

    ## the test for or-and law!!
    # r = BinaryTree("or")
    # r.left_node = BinaryTree("and")
    # r.left_node.left_node = BinaryTree("p")
    # r.left_node.right_node = BinaryTree("q")
    # r.right_node = BinaryTree("c")
    # print("\nthe or_left_and tree:")
    # r.print_binary_tree()

    # r = BinaryTree("or")
    # r.right_node = BinaryTree("and")
    # r.right_node.left_node = BinaryTree("p")
    # r.right_node.right_node = BinaryTree("q")
    # r.left_node = BinaryTree("c")

    # print("\nthe or_right_and tree:")
    # r.print_binary_tree()

    ### the test for and-or-and law
    # r = BinaryTree("or")
    # r.right_node = BinaryTree("and")
    # r.left_node = BinaryTree("and")
    # r.right_node.left_node = BinaryTree("r")
    # r.right_node.right_node = BinaryTree("t")
    # r.left_node.left_node = BinaryTree("p")
    # r.left_node.right_node = BinaryTree("q")
    # print("\nthe and-or-and tree:")
    # r.print_binary_tree()

    # ## the test for neg_rlues.
    # r = BinaryTree("neg")
    # r.left_node = BinaryTree("or")
    # r.left_node.left_node = BinaryTree("neg")
    # r.left_node.right_node = BinaryTree("neg")

    # r.left_node.left_node.left_node = BinaryTree("and")
    # r.left_node.right_node.left_node = BinaryTree("and")

    # r.left_node.left_node.left_node.left_node = BinaryTree("neg")
    # r.left_node.left_node.left_node.right_node = BinaryTree("neg")

    # r.left_node.right_node.left_node.left_node = BinaryTree("neg")
    # r.left_node.right_node.left_node.right_node = BinaryTree("neg")

    # r.left_node.left_node.left_node.left_node.left_node = BinaryTree("p")
    # r.left_node.left_node.left_node.right_node.left_node = BinaryTree("q")

    # r.left_node.right_node.left_node.left_node.left_node = BinaryTree("r")
    # r.left_node.right_node.left_node.right_node.left_node = BinaryTree("t")

    # print("\nthe and-or-and tree:")
    # r.print_binary_tree()

    # r = BinaryTree("neg")
    # r.left_node = BinaryTree("or")
    # # r.left_node.left_node = BinaryTree("neg")
    # r.left_node.right_node = BinaryTree("p")

    # r.left_node.left_node = BinaryTree("and")
    # r.left_node.left_node = BinaryTree("and")

    # r.left_node.left_node.left_node = BinaryTree("neg")
    # r.left_node.left_node.right_node = BinaryTree("neg")

    # r.left_node.left_node.left_node = BinaryTree("neg")
    # r.left_node.left_node.right_node = BinaryTree("neg")

    # r.left_node.left_node.left_node.left_node = BinaryTree("p")
    # r.left_node.left_node.right_node.left_node = BinaryTree("q")

    # r.left_node.left_node.left_node.left_node = BinaryTree("r")
    # r.left_node.left_node.right_node.left_node = BinaryTree("t")

    # print("\nthe and-or-and tree:")
    # r.print_binary_tree()

    ### test for imp_rules
    # r = BinaryTree("imp")
    # r.left_node = BinaryTree("neg")
    # r.left_node.left_node = BinaryTree("p")
    # r.right_node = BinaryTree("q")
    # r.print_binary_tree()

    ### test for iff_rules
    # r = BinaryTree("iff")
    # r.left_node = BinaryTree("neg")
    # r.left_node.left_node = BinaryTree("p")
    # r.right_node = BinaryTree("neg")
    # r.right_node.left_node = BinaryTree("q")
    # r.print_binary_tree()


    # a = CNF('(neg r) imp (neg q)')
    a = CNF(' neg((((neg(nea)) and (neg(ada))) or ((ifc iff n) and (a imp i)) ')
    print(a.prop_list)
    # x = a.or_and(r)
    # x = a.and_or_and(r)
    # a.neg_rules(r)
    # a.neg_neg(r)
    # a.imp_rule(r)
    # a.iff_rule(r)
    # a.or_rules(r)
    # a.morgan_rules(r)
    # print("after converting:")
    # r.print_binary_tree()

    # argv = parserArgument()
    # a = BinaryTree()
    # b = Stack()
    # print(b)
    # print(a)
    # pro_after_CNF = CNF(argv.proposition)
    # print(argv.proposition)


 