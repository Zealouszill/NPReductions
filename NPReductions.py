# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 11:13:51 2019

@author: spencer.stewart
"""

from collections import defaultdict
from functools import reduce
from pulp import LpProblem, LpMinimize, LpMaximize, LpVariable, \
    LpInteger, LpContinuous, LpBinary

def ilp_sat(passedVariables):

    # (['a,-b,c'], [b,d])

    constraints = []
    tempList = []
    dictList = defaultdict(list)

    for i in range(len(passedVariables)):
        tempList += passedVariables[i].split(',')

    # print("This is the tempList", tempList)

    for i in passedVariables:
        for j in range(len(i)):
            dictList[tempList[i]].append(LpVariable(tempList[i] + str(len(constraints)), 0, 1, cat = LpBinary))

    print

    for i in range(len(dictList)):
        print("This is what we printing", dictList[i])


    def createOrVariable(v1, v2):

        result = LpVariable(name = "or" + str(len(constraints)), min = 0, max = 1, cat = LpBinary)
        constraints.append(result >= v1)
        constraints.append(result >= v2)
        constraints.append(result <= v1 + v2)

        return result
    # result = LpBinary()

    lits = "a,-b,c".split(',')
    litvars = list(lit2var[lit] for lit in lits)
    c = reduce(litvars, createOrVariable)




    return lp('max', 1, constraints)

def test_BinaryCircuitTest():
    
    """
    Input will look something similar to this:
        f(x,y,z) = (x or ~y or z)(~x or ~y)(y)
    
    Output will look something like:
        ilp_sat(['a,b,c', '-a,b,-c', '-d,-b', '-a,c', '-b,a'])

    step 1 Find all variables - a, b, c

    for each of those create dictionary. and create negated varibles

    dict[a] points to the LpVariable a

    Find out how many variables we have.
    Loop through each one and assume we have a negative of it.
    If we have A, B, C, then we will have 6 variables in the end.

    Then you create an LpVariable for each of the 6.

    func tools in reduce
    plus(v1, v2):

        return v1 + v2


    assert reduce([5,2,1], plus) == 8
    Pass in list of LpVariables ^^

    Create a CreateOr Function that take in two variables

    input variables are the only ones that need to be binary
    the other variables can be continuous

    Create a new variable for the ORs and the ANDs so that you can create constraints
    in conjunction with that variable.


    """
    # result = ilp_sat(['a,b,c', '-a,b,-c', '-d,-b', '-a,c', '-b,a'])



    result = ilp_sat(['a,-b,c', 'b,c,d'])
    assert result[2] == 1


