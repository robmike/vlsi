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

P = 1
N = 2
D = 3
PND = [0,P,N,D]

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
            cube = [D]*(nvar + 1)
            cube[0] = 0         # not used
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
        
s = StringIO()
x = readdata('part1.cubes')
writedata(x, s)
print s.getvalue()