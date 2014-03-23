#!/usr/bin/python
# -*- coding:Utf-8 -*-


from redbaron import RedBaron
from redbaron.nodes import NameNode, EndlNode, IntNode, AssignmentNode


def test_empty():
    RedBaron("")


def test_is_list():
    assert [] == list(RedBaron(""))


def test_name():
    red = RedBaron("a\n")
    assert len(red) == 2
    assert isinstance(red[0], NameNode)
    assert isinstance(red[1], EndlNode)
    assert red[0].value == "a"


def test_int():
    red = RedBaron("1\n")
    assert isinstance(red[0], IntNode)
    assert red[0].value == 1


def test_assign():
    red = RedBaron("a = 2")
    assert isinstance(red[0], AssignmentNode)
    assert isinstance(red[0].value, IntNode)
    assert red[0].value.value == 2
    assert isinstance(red[0].target, NameNode)
    assert red[0].target.value == "a"


def test_binary_operator():
    red = RedBaron("z +  42")
    assert red[0].value == "+"
    assert isinstance(red[0].first, NameNode)
    assert red[0].first.value == "z"
    assert isinstance(red[0].second, IntNode)
    assert red[0].second.value == 42

    red = RedBaron("z  -      42")
    assert red[0].value == "-"
    assert isinstance(red[0].first, NameNode)
    assert red[0].first.value == "z"
    assert isinstance(red[0].second, IntNode)
    assert red[0].second.value == 42


#def test_while():
    #check_dumps("while a  : pass")


#def test_while_else():
    #check_dumps("while a  : pass\nelse : pass")


#def test_while_indent():
    #check_dumps("while a:\n    pass")


#def test_if():
    #check_dumps("if a:\n    pass")


#def test_if_elif():
    #check_dumps("if a: \n    pass\nelif b: pass")


#def test_if_elif_else():
    #check_dumps("if a: \n    pass\nelif b: pass\nelse :   \n	pouet")


#def test_import():
    #check_dumps("import  a")


#def test_import_madness():
    #check_dumps("import  a.B .   c as  saucisse")


#def test_from_import():
    #check_dumps("from b   import  a  as   rev")


#def test_from_import_special_notation():
    #check_dumps("from a import (b)")
    #check_dumps("from a import (b, c, d)")


#def test_print_empty():
    #check_dumps("print")


#def test_print():
    #check_dumps("print pouet")


#def test_print_madness():
    #check_dumps("print >>  qsd, pouet, zdzd,")


#def test_atom_trailers_call():
    #check_dumps("a.c(b)")


#def test_atom_trailers_call_default():
    #check_dumps("caramba(s, b=2)")


#def test_list_argument():
    #check_dumps("caramba(* a)")


#def test_dict_argument():
    #check_dumps("caramba(** a)")


#def test_list_argument_funcdef():
    #check_dumps("def caramba(* a): pass")


#def test_dict_argument_funcdef():
    #check_dumps("def caramba(** a): pass")


#def test_string():
    #check_dumps("'ama string!'")


#def test_funcdef():
    #check_dumps("def a  ( ) : pass")


#def test_funcdef_indent():
    #check_dumps("def a  ( ) : \n    pass")


#def test_funcdef_parameter():
    #check_dumps("def a  ( b ) : pass")


#def test_funcdef_parameter_named():
    #check_dumps("def a  ( b  , c = qsd ) : pass")


#def test_return():
    #check_dumps("return a")


#def test_getitem():
    #check_dumps("a[ b  ]")


#def test_slice_empty():
    #check_dumps("a[ :  ]")


#def test_slice_classical():
    #check_dumps("a[1: 42]")


#def test_slice_step():
    #check_dumps("a[1: 42:]")
    #check_dumps("a[1: 42    :         3]")


#def test_unitary_operator():
    #check_dumps("- 1")


#def test_unicode_string():
    #check_dumps("u'pouet'")


#def test_raw_string():
    #check_dumps("r'pouet'")


#def test_unicode_raw_string():
    #check_dumps("ur'pouet'")


#def test_binary_string():
    #check_dumps("b'pouet'")


#def test_binary_raw_string():
    #check_dumps("br'pouet'")


#def test_for():
    #check_dumps("for i in pouet : pass")


#def test_for_indent():
    #check_dumps("for i in pouet : \n    pass")


#def test_for_else():
    #check_dumps("for i in pouet : pass\nelse: pass")


#def test_lambda():
    #check_dumps("lambda : x")


#def test_lambda_args():
    #check_dumps("lambda poeut, hompi_dompi: x")


#def test_try_finally():
    #check_dumps("try : pass\nfinally : pass")


#def test_try_except():
    #check_dumps("try : pass\nexcept Exception : pass")


#def test_try_except_comma():
    #check_dumps("try : pass\nexcept Exception ,   d : pass")


#def test_try_except_as():
    #check_dumps("try : pass\nexcept Exception     as   d : pass")


#def test_try_except_finally():
    #check_dumps("try : pass\nexcept Exception : pass\nfinally : pass")


#def test_try_except_finally_else():
    #check_dumps("try : pass\nexcept Exception : pass\nelse: pouet\nfinally : pass")


#def test_comment():
    #check_dumps("# pouet")


#def test_comment_formatting():
    #check_dumps("a # pouet")


#def test_augassign():
    #check_dumps("a &= b")


#def test_call_forth_formatting():
    #check_dumps("set(n for e in s() \n                 if a)")


#def test_boolean_operator():
    #check_dumps("a and b")


#def test_boolean_operator_advanced():
    #check_dumps("a and b or c and d")


#def test_comparison():
    #check_dumps("a < b")


#def test_with():
    #check_dumps("with a : \n    pass")


#def test_with_as():
    #check_dumps("with a as b : \n    pass")


#def test_dict_empty():
    #check_dumps("{   }")


#def test_dict_one():
    #check_dumps("{ a : b  }")


#def test_dict_more():
    #check_dumps("{ a : b   ,\n123  :     'pouet'  }")


#def test_ternary_operator():
    #check_dumps("a   if        b  else      c")


#def test_yield_empty():
    #check_dumps("yield")


#def test_yield():
    #check_dumps("yield a")


#def test_decorator():
    #check_dumps("@pouet\ndef a(): pass")


#def test_decorator_call():
    #check_dumps("@pouet('pouet')\ndef a(): pass")


#def test_class():
    #check_dumps("class A: pass")


#def test_class_parenthesis():
    #check_dumps("class A(): pass")


#def test_class_parenthesis_inherit():
    #check_dumps("class A(B): pass")


#def test_class_parenthesis_inherit_decorated():
    #check_dumps("@pouet\nclass A(B): pass")


#def test_tuple():
    #check_dumps("a  ,  b    , c")


#def test_tuple_parenthesis():
    #check_dumps("( a  ,  b    , c    )")


#def test_return_empty():
    #check_dumps("return")


#def test_list_empty():
    #check_dumps("[   ]")


#def test_list():
    #check_dumps("[ x ]")


#def test_list_more():
    #check_dumps("[ x, r, f, e   , e ]")


#def test_associative_parenthesis():
    #check_dumps("( \n   ( a ) +   ( 1 *    4 )\n ) ")


#def test_fplist():
    #check_dumps("def a((b, c)): pass")


#def test_break():
    #check_dumps("break")


#def test_assert():
    #check_dumps("assert a == b")
    #check_dumps("assert a == b  , c")


#def test_continue():
    #check_dumps("continue")


#def test_raise():
    #check_dumps("raise")
    #check_dumps("raise a")
    #check_dumps("raise a ,   b")
    #check_dumps("raise a ,   b   ,     c")


#def test_del():
    #check_dumps("del a")


#def test_star():
    #check_dumps("from a import *")


#def test_string_chain():
    #check_dumps("'q' 'b'")


#def test_list_comprehension():
    #check_dumps("[ x for   y       in  z      ]")


#def test_list_comprehension_ifs():
    #check_dumps("[ x for   y       in  z   if a   if  qsd  ]")


#def test_list_comprehension_ifs_more():
    #check_dumps("[ x for   y       in  z   if a   if  qsd  for ss in gfgr    ]")


#def test_generator_comprehension():
    #check_dumps("( x for   y       in  z      )")


#def test_generator_comprehension_ifs():
    #check_dumps("( x for   y       in  z   if a   if  qsd  )")


#def test_generator_comprehension_ifs_more():
    #check_dumps("( x for   y       in  z   if a   if  qsd  for ss in gfgr    )")

#if sys.version_info >= (2, 7):
    #def test_dict_comprehension():
        #check_dumps("{ x: z for   y       in  z      }")


    #def test_dict_comprehension_ifs():
        #check_dumps("{ x   : z for   y       in  z   if a   if  qsd  }")


    #def test_dict_comprehension_ifs_more():
        #check_dumps("{ x :z for   y       in  z   if a   if  qsd  for ss in gfgr    }")


    #def test_set_comprehension():
        #check_dumps("{ x for   y       in  z      }")


    #def test_set_comprehension_ifs():
        #check_dumps("{ x    for   y       in  z   if a   if  qsd  }")


    #def test_set_comprehension_ifs_more():
        #check_dumps("{ x  for   y       in  z   if a   if  qsd  for ss in gfgr    }")


#def test_argument_generator_comprehension():
    #check_dumps("a( x for   y       in  z)")


#def test_argument_generator_comprehension_comprehension_ifs():
    #check_dumps("a( x    for   y       in  z   if a   if  qsd)")


#def test_argument_generator_comprehension_comprehension_ifs_more():
    #check_dumps("a(x  for   y       in  z   if a   if  qsd  for ss in gfgr)")


#def test_hexa():
    #check_dumps("0x123")


#def test_octa():
    #check_dumps("0123")


#def test_binary():
    #check_dumps("0b010110101100")


#def test_float():
    #check_dumps("1.2")


#def test_complex():
    #check_dumps("10j")


#def test_float_exponant():
    #check_dumps("1e9")


#def test_semicolon():
    #check_dumps("a;b")


#def test_exec():
    #check_dumps("exec a")


#def test_exec_globals():
    #check_dumps("exec a  in   b")


#def test_exec_globals_locals():
    #check_dumps("exec a  in   b   ,     c")


#def test_global():
    #check_dumps("global a")


#def test_global_more():
    #check_dumps("global a ,   b,    d")


#def test_ellipsis():
    #check_dumps("a[ . .  .]")


#def test_yield_atom_empty():
    #check_dumps("a = ( yield )")


#def test_yield_atom():
    #check_dumps("a = ( yield b )")


#def test_repr():
    #check_dumps("` a  `")


#def test_comment_special_case():
    #check_dumps("d((s)   # Padding\n)")


#def test_from_import_parenthesis_formatting():
    #check_dumps("from a import (\nb, c\n)\n")


#def test_getitem_special_case():
    #check_dumps("[a[...] ]")


#def test_print_tuple():
    #check_dumps("print(pouet, pouet)")


#def test_raise_special():
    #check_dumps("raise   # pouet")


#def test_from_import_star_comment():
    #check_dumps("from a import * # pouet")


#def test_class_formatting():
    #check_dumps("class A(pouet) : \n    pass")


#def test_backslash_not_in_formatting():
    #check_dumps("if a not \\\n      in b: pass")


#def test_try_import_after_colon():
    #check_dumps("try: import stuff\nexcept: pass")
