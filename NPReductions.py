# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 11:13:51 2019

@author: spencer.stewart
"""

from collections import defaultdict
from pulp import LpProblem, LpMinimize, LpMaximize, LpVariable




def test_BinaryCircuitTest():
    
    """
    Input will look something similar to this:
        f(x,y,z) = (x or ~y or z)(~x or ~y)(y)
    
    Output will look something like:
        ilp_sat(['a,b,c', '-a,b,-c', '-d,-b', '-a,c', '-b,a'])
    
    """