# Import module support
# import support
# https://stackoverflow.com/questions/21236824/unresolved-reference-issue-in-pycharm
# right click -> mark directory as source root
from support import print_func
import support as s

# Now you can call defined function that module as follows


print_func('leo')
s.print_func('adam')