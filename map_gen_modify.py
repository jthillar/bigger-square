#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import os

def map_gen(x, y, density):
    print('{}.ox'.format(y))
    result = str(y) + '.ox\n'
    for i in range(int(y)):
        resultTemp = ''
        for j in range(int(x)):
            if (random.randint(0, int(y)) * 2) < int(density):
                print('o', end='')
                resultTemp += 'o'
            else:
                print('.', end='')
                resultTemp += '.'
        print('', end='\n')
        result += resultTemp + '\n'

    i = 1
    while True:
        filePath = str(x) + '_' + str(y) + '_' + str(density) + '_' + str(i)
        if not os.path.isfile(filePath):
            textFile = open(filePath, "w")
            textFile.write(result)
            textFile.close()
            break
        i += 1


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Missing parameters.')
        exit()
    map_gen(*sys.argv[1:4])
