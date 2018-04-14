#!/usr/bin/python
import re
import os, sys
from random import randint, sample, choice

def getId():
    alpha = choice(range(26))
    ret = [choice([1,2])] + sample(range(10),7)
    chk = [v*(8-i) for i,v in enumerate(ret) ]
    chk = int("10987654932210898765431320"[alpha]) + sum(chk)
    chk = (10-chk%10) % 10
    return chr(alpha+ord("A")) + ''.join(map(str,ret)) + str(chk)

def checkId(id):
    i = id
    if not re.match('^[A-Z][12][0-9]{8}$', i): print('pattern not valid'); return False
    a = []; a.extend("10987654932210898765431320")
    c = int(a[ord(i[0])-65]) + int(i[9])
    for x in range(1, 9): c += int(i[x]) * (9 - x)
    if c % 10 != 0:
        # print(id + ', failed');
        return False
    else:
        # print(id + ', passed')
        return True

if __name__ == '__main__':
    needCnt = 1000000

    tmpList = set()
    passCnt = 0
    while True:
        id = getId()
        if checkId(id) and not(id in tmpList):
            tmpList.add(id)
            passCnt+=1

        if passCnt >= needCnt:
            break

    for x in tmpList:
        print(x)

    print(len(tmpList))
