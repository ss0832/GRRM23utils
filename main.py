import sys
import interface

# test program
file = sys.argv[1]
linkjob_dist = interface.LinkJOB2list(file)
interface.list2LinkJOB(file, linkjob_dist)
