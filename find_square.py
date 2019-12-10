#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def printSquare(plate, square, weight):

    # On commence par récupéré les positions du carrées
    plateToPrint = str()
    squarePosition = []
    for i in range(0, square['size']):
        squarePosition += [x + (weight * i) for x in range(square['start'], square['start'] + square['size'])]

    for i, e in enumerate(plate):
        if i in squarePosition:
            plateToPrint += 'x'
        else:
            plateToPrint += e
        if (i + 1) % weight == 0 and i + 1 != len(plate):
            plateToPrint += '\n'

    print(plateToPrint)


def checkFirstLine(firstLine):

    if len(firstLine) < 3:
        return None
    if firstLine[-2:] != '.o':
        return None
    try:
        n = int(firstLine.split('.')[0])
        return n
    except:
        return None


def checkFileAndSaveObstacle(plate):

    # On commence Par checker la première ligne
    plateSplite = plate.split('x\n')

    if len(plateSplite) != 2:
        print('Error File : No plate in file')
        exit()

    nLine = checkFirstLine(plateSplite[0])
    if nLine is None or nLine == 0:
        print('Error File : No plate in file')
        exit()

    nCol = None
    nColTemp = 0
    nLineTemp = 0
    obstacleVec = list()

    # On verifie qu'il y a bien les bons éléments dans le plateau et on vérifie que le nombre de ligne correspond à celui d'entrée
    for i, e in enumerate(plateSplite[1]):
        if e not in ['.', 'o', '\n']:
            print('Error File : Element of plate is wrong')
            exit()
        if e != '\n':
            nColTemp += 1

        else:
            if nCol is None:
                nCol = nColTemp
                nColTemp = 0
                nLineTemp += 1
            elif nCol is not None and nColTemp != nCol:
               print('Error File : Error in columns, element is missing')
               exit()
            else:
                nColTemp = 0
                nLineTemp += 1

    if nLine != nLineTemp:
        print('Error File : No correspondance in number of line')
        exit()

    plate = plateSplite[1].replace('\n', '') # C'est un peu barbare, mais cela me simplifiait le travail de ne pas travail avec les retours lignes
    # On récupère dans un vecteur les positions des obstacles
    for i, e in enumerate(plate):
        if e == 'o':
            obstacleVec.append(i)
    return plate, obstacleVec, nLine, nCol


def find_square(filePath):

    plateFile = open(filePath, 'r')
    plate = plateFile.read()
    plate, obstacleVec, height, weight = checkFileAndSaveObstacle(plate)

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

    printSquare(plate, square, weight)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing Entry File')
        exit()

    for i in range(1, len(sys.argv)):
        find_square(sys.argv[i])
