# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 11:13:51 2019

@author: spencer.stewart
"""

from collections import defaultdict
from functools import reduce
from pulp import LpProblem, LpMinimize, LpMaximize, LpVariable, LpInteger, LpContinuous, LpBinary
import re

def vars(s, low=None, high=None):
    """example creates three variables bounded from 0 to 10:
    a, b, c = vars('a,b,c', 0, 10)
    """
    return tuple(LpVariable(v.strip(), low, high) for v in s.split(','))

def lp(mode, objective, constraints):
    """see lp1 below for an example"""

    if mode.lower() == 'max':
        mode = LpMaximize
    elif mode.lower() == 'min':
        mode = LpMinimize
    prob = LpProblem("", mode)
    prob += objective
    for c in constraints:
        prob += c
    # LpSolverDefault.msg = 1
    print("Prob variables", prob.variables())
    prob.solve()
    return prob, prob.objective.value(), dict((v.name, v.value()) for v in prob.variables())


def ilp_sat(passedVariables):

    passedVariables = (['a,-b,c', 'b,c,d'])

    constraints = []
    allCharactersList = []
    allCharactersSplit = []
    lpVariableList = []
    tempList = []
    totalList = []
    tempSplit = ()
    dictList = defaultdict(list)


    orList = []
    andList = []

    for i in range(len(passedVariables)):
        allCharactersSplit += passedVariables[i].split(',')

    print("This is the allCharactersSplit", allCharactersSplit)
    
    for i in allCharactersSplit:
        print("This is i", i)
        if (len(i) > 1):
            i = re.sub('[-]', '', i)
            tempVar = LpVariable(i, 0, 1, LpContinuous, None)
            allCharactersList.append(tempVar)
        else:
            allCharactersList.append(i)
            
    print("Printing allCharactersList", allCharactersList)

    for i in passedVariables:
        tempSplit = i.split(',')
        for j in tempSplit:
            tempList.append(LpVariable("lp_" + j, 0, 1, cat = LpBinary))
        totalList.append(tempList)
        tempList = []
        print("totalList this is", totalList)


    def createNotConstraints(v):

        result = LpVariable(name = v + str(len(constraints)), lowBound = 0, upBound = 1, cat = LpContinuous)
        # constraints.append(result == 1 - v) # you get this error because V isn't a LP function.


    def createOrVariable(v1, v2):

        result = LpVariable(name = "or" + str(len(constraints)), lowBound = 0, upBound = 1, cat = LpContinuous)
        constraints.append(result >= v1)
        constraints.append(result >= v2)
        constraints.append(result <= v1 + v2)

        return result

    def createAndVariable(v1, v2):

        result = LpVariable(name = "and" + str(len(constraints)), lowBound = 0, upBound = 1, cat = LpContinuous)
        constraints.append(result <= v1)
        constraints.append(result <= v2)
        constraints.append(result >= v1 + v2 + 1)

        return result

    for i in allCharactersList:
        result = LpVariable(i, 0, 1, cat=LpBinary)
        # print("This is i", i)
        dictList[i] = result

    for i in dictList:
        createNotConstraints(i)
        print("This is what we printing", dictList[i])


    for i in totalList:
        orList.append(reduce(createOrVariable, i))

    print("This is orClauses", orList)

    reduce(createAndVariable, orList)

    print("These are the constraints:")
    print(constraints)

    # lits = "a,-b,c".split(',')
    # litvars = list(lit2var[lit] for lit in lits)
    #
    # print("This is litvars", litvars)
    #
    # c = reduce(litvars, createOrVariable)


    for i in constraints:
        print(i)

    # print("List of constraints", constraints)

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


    assert reduce(plus, [5,2,1]) == 8


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


def test_reduce():

    def plus(v1, v2):
        return v1 + v2

    assert reduce(plus, [5, 2, 1]) == 8
