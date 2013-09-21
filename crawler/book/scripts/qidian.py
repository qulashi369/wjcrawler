import os


def get_nopict_bid(path="."):
    picts = os.listdir(path)
    print picts
    temppicts = [int(v[:-4]) for v in picts]
    temppicts.sort()
    fixed = 1
    nonpict_books = []
    for curindex, v in enumerate(temppicts):
        if curindex + 1 == len(picts):
            break
        curfix = temppicts[curindex + 1] - temppicts[curindex]
        if curfix > fixed:
            cur_val = v
            for num in curfix:
                nonpict_books.append(cur_val)
                cur_val += 1
    return nonpict_books

print get_nopict_bid("../pics/")
