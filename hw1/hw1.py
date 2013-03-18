import numpy as np
import random
import copy
import heapq
import progressbar as pb
from collections import defaultdict, Counter
from pprint import pprint
from StringIO import StringIO

import cProfile

import pdb, sys

# debug shit (from stackexchange)
def info(type, value, tb):
   if hasattr(sys, 'ps1') or not sys.stderr.isatty():
      # we are in interactive mode or we don't have a tty-like
      # device, so we call the default hook
      sys.__excepthook__(type, value, tb)
   else:
      import traceback, pdb
      # we are NOT in interactive mode, print the exception...
      traceback.print_exception(type, value, tb)
      print
      # ...then start the debugger in post-mortem mode.
      pdb.pm()

sys.excepthook = info

P = 1
N = 2
D = 3
PND = [0,P,N,D]

def readdata(infile): 
    cubelist = []
    with open(infile, 'r') as f:
        nvar = int(f.readline())
        ncubes = int(f.readline())
        for i,line in enumerate(f):
            terms = line.split()
            if not terms:
                continue
            n = terms.pop(0)
            cube = [D]*(nvar + 1) # 0th element not used
            for x in terms:
                x = int(x)
                cube[abs(x)] = x > 0 and P or N
            cubelist.append(cube)
    return cubelist

def writedata(cubelist, out):
    nvar = len(cubelist[0]) - 1
    ncubes = len(cubelist)
    out.write('%i\n%i\n' % (nvar, ncubes))
    for cube in cubelist:
        out.write(len([x for x in cube if x != D]) - 1)
        for i,x in enumerate(cube[1:]):
            if x != D:
                out.write(' ')
                out.write(x == P and i+1 or -(i+1))
        out.write('\n')
    return out

def negate(cube):
    return [x == P and N or x == N and P or D for x in cube]

def split_var(cubelist):
    nvar = len(cubelist[0]) - 1
    # count frequency of positive and negative occurrences
    pos = [0]*(nvar+1)
    neg = [0]*(nvar+1)
    for c in cubelist:
        for i,x in enumerate(c):
            if x == P:
                pos[i] += 1
            elif x == N:
                neg[i] += 1
    # Are there binate variables?
    counts = [x + y for (x,y) in zip(pos,neg)]
    if any([x > 0 and y > 0 for (x,y) in zip(pos,neg)]):
        idx = [i for i,val in enumerate(counts) if val == max(counts)]
        dcount = [abs(x-y) for (x,y) in zip(pos,neg)]
        maxdcount = max([d for i,d in enumerate(dcount) if i in idx])
        idx = [i for i in idx if dcount[i] == maxdcount]
        assert(idx[0] == min(idx))
        idx = idx[0]            # break ties with first index
        return idx
    else:                       # unates only
        return counts.index(max(counts))

    

def complement(cubelist, nvar):
    one = [D]*(nvar + 1)
    if len(cubelist) == 0:
        return one
    if one in cubelist:
        return []
    if len(cubelist) == 1:
        cube = cubelist[0]
        outcl = []
        for i,x in enumerate(cube):
            if x != D:
                c = [D]*(nvar+1)
                c[i] = x == P and N or x == N and P
                outcl.append(c)
        return outcl

    x = split_var(cubelist)
        
s = StringIO()
x = readdata('part1.cubes')
pprint(x)
writedata(x, s)
print s.getvalue()

print complement([], 5)         # 1
print complement([[D, D, D, D]], 3)
print complement([x[0]], len(x[0])-1)
print split_var(x)