import sys

start = int(sys.argv[1])
end = int(sys.argv[2])

for i in range(start, end):
    print "%d:%d" % (i, i)
