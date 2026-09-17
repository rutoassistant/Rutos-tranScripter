#
# Created on Mon Jun 14 2021
#
# The MIT License (MIT)
# Copyright (c) 2021 Vishnu Suresh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#




class ArithmeticEnv:
    def __init__(self):
        pass
    
    '''
    env_variables :- is a list of variables which act a variables with out '$' in the program

    '''
    env_Variables = ["result"]
    name_of_Env="ArithmeticEnv"

    '''
    Word As Function :- In here each word is assigned to an python function, which returns an python code as a string.
    In some sonorous some words have no functionalities in that case return "None"

    '''

    @staticmethod
    def addFun(*args):
        parts = [f'{x if "$" not in x else x[1:]}' for x in args]
        return f'result =int({" + ".join(parts)})'

    @staticmethod
    def multiplyFun(*args):
        parts = [f'{x if "$" not in x else x[1:]}' for x in args]
        return f'result ={" * ".join(parts)}'

    @staticmethod
    def divideFun(*args):
        parts = [f'{x if "$" not in x else x[1:]}' for x in args]
        return f'result =int({" / ".join(parts)})'

    @staticmethod
    def subtractFun(*args):
        parts = [f'{x if "$" not in x else x[1:]}' for x in args]
        return f'result ={" - ".join(parts)}'

    @staticmethod
    def powerFun(*args):
        if len(args) != 2:
            raise Exception("power requires exactly two arguments")
        a = f'{args[0] if "$" not in args[0] else args[0][1:]}'
        b = f'{args[1] if "$" not in args[1] else args[1][1:]}'
        return f'result = {a} ** {b}'

    @staticmethod
    def moduloFun(*args):
        if len(args) != 2:
            raise Exception("modulo requires exactly two arguments")
        a = f'{args[0] if "$" not in args[0] else args[0][1:]}'
        b = f'{args[1] if "$" not in args[1] else args[1][1:]}'
        return f'result = {a} % {b}'

    @staticmethod
    def ltFun(*args):
        if len(args) != 2:
            raise Exception("lt requires exactly two arguments")
        a = f'{args[0] if "$" not in args[0] else args[0][1:]}'
        b = f'{args[1] if "$" not in args[1] else args[1][1:]}'
        return f'result = {a} < {b}'

    @staticmethod
    def gtFun(*args):
        if len(args) != 2:
            raise Exception("gt requires exactly two arguments")
        a = f'{args[0] if "$" not in args[0] else args[0][1:]}'
        b = f'{args[1] if "$" not in args[1] else args[1][1:]}'
        return f'result = {a} > {b}'

    @staticmethod
    def eqFun(*args):
        if len(args) != 2:
            raise Exception("eq requires exactly two arguments")
        a = f'{args[0] if "$" not in args[0] else args[0][1:]}'
        b = f'{args[1] if "$" not in args[1] else args[1][1:]}'
        return f'result = {a} == {b}'

    @staticmethod
    def neFun(*args):
        if len(args) != 2:
            raise Exception("ne requires exactly two arguments")
        a = f'{args[0] if "$" not in args[0] else args[0][1:]}'
        b = f'{args[1] if "$" not in args[1] else args[1][1:]}'
        return f'result = {a} != {b}'

    @staticmethod
    def leFun(*args):
        if len(args) != 2:
            raise Exception("le requires exactly two arguments")
        a = f'{args[0] if "$" not in args[0] else args[0][1:]}'
        b = f'{args[1] if "$" not in args[1] else args[1][1:]}'
        return f'result = {a} <= {b}'

    @staticmethod
    def geFun(*args):
        if len(args) != 2:
            raise Exception("ge requires exactly two arguments")
        a = f'{args[0] if "$" not in args[0] else args[0][1:]}'
        b = f'{args[1] if "$" not in args[1] else args[1][1:]}'
        return f'result = {a} >= {b}'

    @staticmethod
    def incrementFun(*args):
        if len(args) != 1:
            raise Exception("increment requires exactly one argument")
        a = f'{args[0] if "$" not in args[0] else args[0][1:]}'
        return f'result = {a} + 1'

    @staticmethod
    def decrementFun(*args):
        if len(args) != 1:
            raise Exception("decrement requires exactly one argument")
        a = f'{args[0] if "$" not in args[0] else args[0][1:]}'
        return f'result = {a} - 1'

    @staticmethod
    def storeFun(*args):
        list_to_print = []
        for value in reversed(args):
            if "$" in value:
                if "~" == value[1:2]:
                    # print(f'{value[1:]}')
                    list_to_print.append(f'"{value[2:]}"')
                else:
                    list_to_print.append(value[1:])
        if len(list_to_print) == 2:
            # if str(args[1]).isnumeric():
            # result = f'{args[0] if "$" not in args[0] else args[0][1:]}={args[1] if "$" not in args[1] else args[1][1:]}'
            result = f'{list_to_print[1]}={list_to_print[0]}'
            # else:
            # raise Exception("Second argument must be integer")
            return result
        else:
            raise Exception("Only One variable and one Integer is support")

    @staticmethod
    def theFun(*args):
        return None

    @staticmethod
    def withFun(*args):
        return None

    @staticmethod
    def thenFun(*args):
        return None

    @staticmethod
    def toFun(*args):
        return None

    @staticmethod
    def inFun(*args):
        return None

    @staticmethod
    def andFun(*args):
        return None

    @staticmethod
    def commaFun(*args):
        return ArithmeticEnv.andFun(*args)

    @staticmethod
    def byFun(*args):
        return None

    @staticmethod
    def stringFun(*args):
        return None
    
    @staticmethod
    def fromFun(*args):
        return None

    @staticmethod
    def printFun(*args):
        list_to_print = []
        for value in reversed(args):
            if "$" in value:
                if "~" == value[1:2]:
                    # print(f'{value[1:]}')
                    list_to_print.append(f'"{value[2:]}"')
                else:
                    list_to_print.append(value[1:])
        result = " ".join(
            ["print(", *[f'{x},' for x in list_to_print], ")"])
        return result

    @staticmethod
    def displayFun(*args):
        return ArithmeticEnv.printFun(*args)

    '''
    env_Words_and_WordAsFunction :- is a key value paired Dictionary which each key corresponds to word that accepted by the ENV
    and the value is the function that defined 

    '''
    env_Words_and_WordAsFunction = {"add": addFun.__func__, "and": andFun.__func__, ",": commaFun.__func__, "print": printFun.__func__,
                                    "multiply": multiplyFun.__func__, "store": storeFun.__func__, "to": toFun.__func__, "in": inFun.__func__, "divide": divideFun.__func__, "by": byFun.__func__,
                                    "display": displayFun.__func__, "the": theFun.__func__, 'then': thenFun.__func__, 'with': withFun.__func__, "string": stringFun.__func__, "subtract": subtractFun.__func__,"from":fromFun.__func__,
                                    "power": powerFun.__func__, "modulo": moduloFun.__func__, "lt": ltFun.__func__, "gt": gtFun.__func__, "eq": eqFun.__func__, "ne": neFun.__func__, "le": leFun.__func__, "ge": geFun.__func__,
                                    "increment": incrementFun.__func__, "decrement": decrementFun.__func__}
