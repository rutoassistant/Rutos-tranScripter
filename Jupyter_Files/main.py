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

# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#Importing Needed Libaries
import nltk
import numpy as np

# %%
#importing data for nltk
nltk.download('punkt')


# %%
# Input String
inputStr='''
store 2 in $v1 .
add 3, 5 and $v1 .
print result.

'''
print("\nInput String :-\n",inputStr)
# inputStr


# %%
#making Tokens of input
tokenizeInput=np.array(nltk.word_tokenize(inputStr))
print("\nTokenzied Input :- \n",tokenizeInput,"\n")


# %%
# CustomTree and MakeTape

class CustomTree:
    def __init__(self):
        self.left=None
        self.right=None
        self.data=None

    def insertNode(self,value):
        if self.data is None:
            self.data=value
        elif self.right is None:
            # print("right is none ",value)
            self.right=CustomTree()
            self.right.insertNode(value=value)
        else:
            if "$" in self.right.data:
                # print("right is not none and $ ",value)
                temp=self.right
                self.right=CustomTree()
                self.right.insertNode(value=value)
                self.right.left=temp
            else:
                # print("right is not none ",value)
                self.right.insertNode(value)
    def PrintTree(self,nodePostion="root",height=0):
        print(f'{self.data} : {nodePostion}, Height : {height}'),
        if self.left:
            self.left.PrintTree(nodePostion="left",height=height+1)
        if self.right:
            self.right.PrintTree(nodePostion="right",height=height+1)
    def makeTape(self):
        tape=[]
        while self.data is not None:
            tape.append(self.data)
            if self.left is not None:
                tape.append(self.left.data)
            if self.right is not None:
                self=self.right
            else:
                break
        return tape

# def makeTape(node:CustomTree):
#     tape=[]
#     while node.data is not None:
#         tape.append(node.data)
#         if node.left is not None:
#             tape.append(node.left.data)
#         if node.right is not None:
#             node=node.right
#         else:
#             break
#     return tape


# %%
#Word as function For Arthimetic Env
class ArithameticEnv:
    def __init__(self):
        pass
    @staticmethod
    def addFun(*args):
        result =" ".join(["result =", *[f'{x if "$" not in x else x[1:]} +' for x in args]])
        result=result[:-1]
        return result
    @staticmethod
    def multiplyFun(*args):
        result =" ".join(["result =", *[f'{x if "$" not in x else x[1:]} *' for x in args]])
        result=result[:-1]
        return result
    @staticmethod
    def divideFun(*args):
        result =" ".join(["result =", *[f'{x if "$" not in x else x[1:]} /' for x in args]])
        result=result[:-1]
        return result
    @staticmethod
    def storeFun(*args):
        if len(args)== 2:
            # if str(args[1]).isnumeric():
            result=f'{args[0] if "$" not in args[0] else args[0][1:]}={args[1] if "$" not in args[1] else args[1][1:]}'
            # else:
                # raise Exception("Second argument must be integer")
            return result
        else:
            raise Exception("Only One variable and one Integer is support")
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
        ArithameticEnv.andFun(*args)

    @staticmethod
    def byFun(*args):
        return None
    @staticmethod
    def printfun(*args):
        result =" ".join(["print(", *[f'{x if "$" not in x else x[1:]}' for x in args],")"])
        return result
    env_Variables=["result"]
    env_Words_and_WordAsFunction={"add":addFun.__func__,"and":andFun.__func__,",":commaFun.__func__,"print":printfun.__func__,"multiply":multiplyFun.__func__,"store":storeFun.__func__,"to":toFun.__func__,"in":inFun.__func__,"divide":divideFun.__func__,"by": byFun.__func__}
# ArithameticEnv.addFun("v1","v2")
#ArithameticEnv.addFun("$v1","v1")
# ArithameticEnv.env_Words_and_WordAsFunction['add']("$v1","v1")


# %%
# Making of Tape from Sentence
global_Tape=[]
itreate_each_word=iter(tokenizeInput)
catch_variable_value=False
end_Of_a_Sentence=True
node=None
try:
    while True:
        current_Word=next(itreate_each_word)
        if current_Word == "$" and not catch_variable_value:
            catch_variable_value=True
        elif current_Word == "." and not end_Of_a_Sentence:
            end_Of_a_Sentence=True
            print("\nCustom Tree Stracture of the current Sentence :- \n")
            node.PrintTree()
            tape=node.makeTape()
            global_Tape.append(tape)
            print("\nEnd of a sentence","\nTape :- \n",tape,"\n")
        else:
            if end_Of_a_Sentence:
                print("\nStarting of a sentence\n")
                end_Of_a_Sentence=False
                node=CustomTree()
            elif catch_variable_value:
                catch_variable_value=False
                current_Word="$"+current_Word
            elif str(current_Word).isnumeric() or current_Word in ArithameticEnv.env_Variables:
                current_Word="$"+current_Word
            node.insertNode(current_Word)
            # print(current_Word)
except StopIteration:
    print("\nEnd of All the lines\n")
    print("\nGlobal Tape :-\n",global_Tape)
    pass


# %%
#The machice to Transfer the natural languae to Python code
pythonCode=[]
varibleBuffer=[]
for sentenceTape in global_Tape:
    varibleBuffer=[]
    for word in reversed(sentenceTape):
        if "$" in word :
            varibleBuffer.append(word)
        else:
            result=ArithameticEnv.env_Words_and_WordAsFunction[word](*varibleBuffer)
            if result is not None:
               pythonCode.append(result)
# pythonCode





# %%
print("\npython code Exected Output\n")
exec("\n".join(pythonCode))


# %%



