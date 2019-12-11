#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def printSquare(plate, square, weight, squareElement):

    # On commence par récupéré les positions du carrées
    plateToPrint = str()
    squarePosition = []
    for i in range(0, square['size']):
        squarePosition += [x + (weight * i) for x in range(square['start'], square['start'] + square['size'])]

    for i, e in enumerate(plate):
        if i in squarePosition:
            plateToPrint += squareElement
        else:
            plateToPrint += e
        if (i + 1) % weight == 0 and i + 1 != len(plate):
            plateToPrint += '\n'

    print(plateToPrint, end='')


def checkFirstLine(firstLine):

    emptyElement = firstLine[-3]
    obstacleElement = firstLine[-2]
    squareElement = firstLine[-1]
    try:
        n = int(firstLine.split(emptyElement)[0])
        return n, emptyElement, obstacleElement, squareElement
    except:
        return None, emptyElement, obstacleElement, squareElement


def checkFileAndSaveObstacle(plate):

    # On commence Par checker la première ligne
    firstLine = plate.split('\n')[0]

    if len(firstLine) < 4:
        print('Map Error', end='')
        exit()

    nLine, emptyElement, obstacleElement, squareElement = checkFirstLine(firstLine)
    if nLine is None or nLine == 0:
        print('Map Error', end='')
        exit()

    nCol = None
    nColTemp = 0
    nLineTemp = 0
    obstacleVec = list()
    plate = plate.split(squareElement+'\n')[1]

    # On verifie qu'il y a bien les bons éléments dans le plateau et on vérifie que le nombre de ligne correspond à celui d'entrée
    for i, e in enumerate(plate):
        if e not in [emptyElement, obstacleElement, '\n']:
            print('Map Error', end='')
            exit()
        if e != '\n':
            nColTemp += 1

        else:
            if nCol is None:
                nCol = nColTemp
                nColTemp = 0
                nLineTemp += 1
            elif nCol is not None and nColTemp != nCol:
               print('Map Error', end='')
               exit()
            else:
                nColTemp = 0
                nLineTemp += 1

    if nLine != nLineTemp or nLine < 1 or nCol < 2:
        print('Map Error', end='')
        exit()

    plate = plate.replace('\n', '') # C'est un peu barbare, mais cela me simplifiait le travail de ne pas travail avec les retours lignes
    # On récupère dans un vecteur les positions des obstacles
    for i, e in enumerate(plate):
        if e == obstacleElement:
            obstacleVec.append(i)
    return plate, obstacleVec, nLine, nCol, squareElement


def find_square(filePath):

    try:
        plateFile = open(filePath, 'r')
        plate = plateFile.read()
    except:
        print('Map Error', end='')
        exit()

    plate, obstacleVec, height, weight, squareElement = checkFileAndSaveObstacle(plate)

    # Varible qui garde en mémoire le plus gros carré
    #  - start : pointe haute gauche du carré
    #  - size : longueur du coté du carré
    square = {'start': 0, 'size': 0}

    leftTopCorner = 0
    count = 0
    i = 0

    # L'idée est d'agrandir les carrés de 1 en 1 jusqu'à ce qu'on touche un obstacle. Une fois l'obstacle touché, on
    # recréé un carré de 1*1 après l'obstacle puis on réagrandit. On va parcourir tout le plateau en gardant le
    # plus gros carré ()
    while i < len(plate):
        if (leftTopCorner + count) % weight == 0:
            leftTopCorner += count
            count = 0

        # on récupère les 4 points du carrées
        rightTopCorner = leftTopCorner + count
        leftBottomCorner = leftTopCorner + weight * count
        if leftBottomCorner > len(plate):
            break
        rightBottomCorner = leftBottomCorner + count

        # On liste les point des droite de droite et du bas du carrés et on regarde si un obstacle y est
        rightPoints = [x for x in range(rightTopCorner, rightBottomCorner + 1, weight) if x in obstacleVec]
        bottomPoints = [x for x in range(leftBottomCorner, rightBottomCorner + 1) if x in obstacleVec]
        obstaclePoint = rightPoints + bottomPoints

        if len(obstaclePoint) == 0:
            count += 1
            if count > square['size']: # On ne regarde que si le carré est plus grand pour garder celui le plus en haut à gauche
                square = {'start': leftTopCorner, 'size': count}

        else:
            # S'il y a un obstacle on replace un nouveau carré. Il faut faire attention à remettre sur la gauche s'il le faut
            leftTopCorner = (leftTopCorner // weight) * weight + (obstaclePoint[0] % weight + 1)
            count = 0

        i += 1

    printSquare(plate, square, weight, squareElement)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing Entry File')
        exit()

    for i in range(1, len(sys.argv)):
        try:
            find_square(sys.argv[i])
        except:
            pass
        print('\n') if i != len(sys.argv) - 1 else print('')

