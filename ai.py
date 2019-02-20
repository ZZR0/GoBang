# Author:ZZR


import numpy as np
import random
import time
import getopt
import sys

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0

LIVE_ONE = 10
LIVE_TWO = 100
LIVE_THREE = 1000
LIVE_TWO_THREE = 50000
LIVE_FOUR = 100000
LIVE_FIVE = 10000000
DEAD_ONE = 1
DEAD_TWO = 10
DEAD_THREE = 100
DEAD_FOUR = 10000

MAX = LIVE_FIVE * 10
MIN = -MAX

LENGTH = 15
Stept = 0
LIMIT = 10

DirScoreCache = [[[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]for _ in range(15)] for _ in range(5)] for _ in range(2)]
DirScoreCache = np.array(DirScoreCache)

random.seed(0)
#don't change the class name
class AI(object):
    #chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #You are white or black
        self.color = color
        #the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        LENGTH = chessboard_size

    # If your are the first, this function will be used.
    def first_chess(self):
        assert self.color == COLOR_BLACK
        self.candidate_list.clear()
        #==================================================================
        #Here you can put your first piece
        #for example, you can put your piece on sun（天元）
        self.candidate_list.append((self.chessboard_size//2,self.chessboard_size//2))
        self.chessboard[self.candidate_list[-1][0], self.candidate_list[-1][0]] = self.color

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        #==================================================================
        #To write your algorithm here
        #Here is the simplest sample:Random decision

        start = time.time()

        blackscoreboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        whitescoreboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)

        init(chessboard, blackscoreboard, whitescoreboard)
        point = []
        # try:
        #     point = vct(chessboard, blackscoreboard, whitescoreboard, self.color, 10)
        # except:
        #     pass
        # point = vct(chessboard, blackscoreboard, whitescoreboard, self.color, 10)
        if point:
            point = point[0]
            self.candidate_list.clear()
            self.candidate_list.append((point[0],point[1]))
            new_pos = (point[0],point[1])
        else:
            idx = sortPos(chessboard, blackscoreboard, whitescoreboard, self.color)
            # print(idx)
            if idx:
                self.candidate_list.append((idx[0][0],idx[0][1]))
                new_pos = (idx[0][0],idx[0][1])
                deep = 8
                z = np.where(chessboard == 0)
                z = list(zip(z[0], z[1]))
                Stept = 226 - len(z)
                if Stept>180:
                    deep = 2
                point = deepFind(chessboard, blackscoreboard, whitescoreboard, idx, self.color, deep)
                self.candidate_list.clear()
                self.candidate_list.append(point)
                new_pos = point
            else:
                self.candidate_list.append((7, 7))
                new_pos = (7, 7)
        #new_pos = deepFind(idx, self.color, 1)
        run_time = (time.time() - start)
        #==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        #If not, return error.
        assert chessboard[new_pos[0],new_pos[1]]==0
        #Add your decision into candidate_list, Records the chess board
        # self.candidate_list.append(new_pos)

def equal(a, b):
    b = b or 0.01
    if b >= 0:
        return a >= b / 1.15 and a <= b * 1.15
    else:
        return a >= b * 1.15 and a <= b / 1.15

def great(a, b):
    if b >= 0:
        return a >= (b + 0.1) * 1.15
    else:
        return a >= (b + 0.1) / 1.15

def greatOrEqual(a, b):
    return equal(a, b) or great(a, b)

def changeColour(color):
    if color == COLOR_BLACK:
        return COLOR_WHITE
    elif color == COLOR_WHITE:
        return COLOR_BLACK
    else:
        return COLOR_NONE

#计算棋型分数
def pointScore(count, dead, empty=0):

    if empty <= 0:
        if count >= 5: return LIVE_FIVE
        if dead == 0:
            if count == 1: return LIVE_ONE
            elif count == 2: return LIVE_TWO
            elif count == 3: return LIVE_THREE
            elif count == 4: return LIVE_FOUR
        elif dead == 1:
            if count == 1: return DEAD_ONE
            elif count == 2: return DEAD_TWO
            elif count == 3: return DEAD_THREE
            elif count == 4: return DEAD_FOUR

    elif empty == 1 or empty == count-1:
        if count >= 6: return LIVE_FIVE
        if dead == 0:
            if count == 2: return LIVE_TWO/2
            elif count == 3: return LIVE_THREE
            elif count == 4: return DEAD_FOUR
            elif count == 5: return LIVE_FOUR
        elif dead == 1:
            if count == 2: return DEAD_TWO
            elif count == 3: return DEAD_THREE
            elif count == 4: return DEAD_FOUR
            elif count == 5: return LIVE_FOUR

    elif empty == 2 or empty == count-2:
        if count >= 7: return LIVE_FIVE
        if dead == 0:
            if count == 3: return LIVE_THREE
            elif count == 4: return LIVE_THREE
            elif count == 5: return DEAD_FOUR
            elif count == 6: return LIVE_FOUR
        elif dead == 1:
            if count == 3: return DEAD_THREE
            elif count == 4: return DEAD_FOUR
            elif count == 5: return DEAD_FOUR
            elif count == 6: return LIVE_FOUR
        elif dead == 2:
            if count == 4: return DEAD_FOUR
            elif count == 5: return DEAD_FOUR
            elif count == 6: return DEAD_FOUR

    elif empty == 3 or empty == count-3:
        if count >= 8: return LIVE_FIVE
        if dead == 0:
            if count == 4: return LIVE_THREE
            elif count == 5: return LIVE_THREE
            elif count == 6: return DEAD_FOUR
            elif count == 7: return LIVE_FOUR
        elif dead == 1:
            if count == 4: return DEAD_FOUR
            elif count == 5: return DEAD_FOUR
            elif count == 6: return DEAD_FOUR
            elif count == 7: return LIVE_FOUR
        elif dead == 2:
            if count == 4: return DEAD_FOUR
            elif count == 5: return DEAD_FOUR
            elif count == 6: return DEAD_FOUR
            elif count == 7: return DEAD_FOUR

    elif empty == 4 or empty == count-4:
        if count >= 9: return LIVE_FIVE
        if dead == 0:
            if count == 5: return LIVE_FOUR
            elif count == 6: return LIVE_FOUR
            elif count == 7: return LIVE_FOUR
            elif count == 8: return LIVE_FOUR
        elif dead == 1:
            if count == 4: return DEAD_FOUR
            elif count == 5: return DEAD_FOUR
            elif count == 6: return DEAD_FOUR
            elif count == 7: return DEAD_FOUR
            elif count == 8: return LIVE_FOUR
        elif dead == 2:
            if count == 5: return DEAD_FOUR
            elif count == 6: return DEAD_FOUR
            elif count == 7: return DEAD_FOUR
            elif count == 8: return DEAD_FOUR

    elif empty == 5 or empty == count-5: return LIVE_FIVE

    return 0

#计算棋面得分
def getScore(chessboard, r, c, color, dir=0):
    result = 0
    empty = 0
    count = 0
    dead = 0
    revCount = 0

    def reset():
        return [1, 0, -1, 0]

    if dir == 0 or dir == 1:
        [count, dead, empty, revCount] = reset()

        # 水平方向
        for i in range(c + 1, LENGTH + 1):
            if i >= LENGTH:
                dead += 1
                break
            p = chessboard[r][i]
            if p == COLOR_NONE:
                if empty == -1 and i < LENGTH - 1 and chessboard[r][i + 1] == color:
                    empty = count
                    continue
                else:
                    break
            if p == color:
                count += 1
                continue
            else:
                dead += 1
                break

        for i in range(c - 1, -2, -1):
            if i < 0:
                dead += 1
                break
            p = chessboard[r][i]
            if p == COLOR_NONE:
                if empty == -1 and i > 0 and chessboard[r][i - 1] == color:
                    empty = 0
                    continue
                else:
                    break
            if p == color:
                revCount += 1
                if empty != -1: empty += 1
                continue
            else:
                dead += 1
                break

        count += revCount
        if color == COLOR_BLACK:
            DirScoreCache[0][1][r][c] = pointScore(count, dead, empty)
        else:
            DirScoreCache[1][1][r][c] = pointScore(count, dead, empty)


    if dir == 0 or dir == 2:
        [count, dead, empty, revCount] = reset()

        # 竖直方向
        for i in range(r + 1, LENGTH + 1):
            if i >= LENGTH:
                dead += 1
                break
            p = chessboard[i][c]
            if p == COLOR_NONE:
                if empty == -1 and i < LENGTH - 1 and chessboard[i + 1][c] == color:
                    empty = count
                    continue
                else:
                    break
            if p == color:
                count += 1
                continue
            else:
                dead += 1
                break

        for i in range(r - 1, -2, -1):
            if i < 0:
                dead += 1
                break
            p = chessboard[i][c]
            if p == COLOR_NONE:
                if empty == -1 and i > 0 and chessboard[i - 1][c] == color:
                    empty = 0
                    continue
                else:
                    break
            if p == color:
                revCount += 1
                if empty != -1: empty += 1
                continue
            else:
                dead += 1
                break

        count += revCount
        if color == COLOR_BLACK:
            DirScoreCache[0][2][r][c] = pointScore(count, dead, empty)
        else:
            DirScoreCache[1][2][r][c] = pointScore(count, dead, empty)


    if dir == 0 or dir == 3:
        [count, dead, empty, revCount] = reset()

        # 右下方向
        for i in range(1, LENGTH + 1):
            new_r = r + i
            new_c = c + i
            if new_r >= LENGTH or new_c >= LENGTH:
                dead += 1
                break
            p = chessboard[new_r][new_c]
            if p == COLOR_NONE:
                if empty == -1 and new_r < LENGTH - 1 and new_c < LENGTH - 1 and chessboard[new_r + 1][
                    new_c + 1] == color:
                    empty = count
                    continue
                else:
                    break
            if p == color:
                count += 1
                continue
            else:
                dead += 1
                break

        for i in range(1, LENGTH + 1):
            new_r = r - i
            new_c = c - i
            if new_r < 0 or new_c < 0:
                dead += 1
                break
            p = chessboard[new_r][new_c]
            if p == COLOR_NONE:
                if empty == -1 and new_r > 0 and new_c > 0 and chessboard[new_r - 1][new_c - 1] == color:
                    empty = 0
                    continue
                else:
                    break
            if p == color:
                revCount += 1
                if empty != -1: empty += 1
                continue
            else:
                dead += 1
                break

        count += revCount
        if color == COLOR_BLACK:
            DirScoreCache[0][3][r][c] = pointScore(count, dead, empty)
        else:
            DirScoreCache[1][3][r][c] = pointScore(count, dead, empty)


    if dir == 0 or dir == 4:
        [count, dead, empty, revCount] = reset()

        # 右上方向
        for i in range(1, LENGTH + 1):
            new_r = r + i
            new_c = c - i
            if new_r >= LENGTH or new_c >= LENGTH or new_c < 0 or new_r < 0:
                dead += 1
                break
            p = chessboard[new_r][new_c]
            if p == COLOR_NONE:
                if empty == -1 and new_r < LENGTH - 1 and new_c > 0 and chessboard[new_r + 1][
                    new_c - 1] == color:
                    empty = count
                    continue
                else:
                    break
            if p == color:
                count += 1
                continue
            else:
                dead += 1
                break

        for i in range(1, LENGTH + 1):
            new_r = r - i
            new_c = c + i
            if new_r >= LENGTH or new_c >= LENGTH or new_c < 0 or new_r < 0:
                dead += 1
                break
            p = chessboard[new_r][new_c]
            if p == COLOR_NONE:
                if empty == -1 and new_r > 0 and new_c < LENGTH - 1 and chessboard[new_r - 1][
                    new_c + 1] == color:
                    empty = 0
                    continue
                else:
                    break
            if p == color:
                revCount += 1
                if empty != -1: empty += 1
                continue
            else:
                dead += 1
                break

        count += revCount
        if color == COLOR_BLACK:
            DirScoreCache[0][4][r][c] = pointScore(count, dead, empty)
        else:
            DirScoreCache[1][4][r][c] = pointScore(count, dead, empty)

    if color == COLOR_BLACK:
        result = DirScoreCache[0][1][r][c] + DirScoreCache[0][2][r][c] + DirScoreCache[0][3][r][c] + \
                 DirScoreCache[0][4][r][c]
    else:
        result = DirScoreCache[1][1][r][c]+DirScoreCache[1][2][r][c]+DirScoreCache[1][3][r][c]+DirScoreCache[1][4][r][c]
    return fix_score(result)

#加权冲四活三分数
def fix_score(s):
    if s<LIVE_FOUR and s>DEAD_FOUR:
        if s>=DEAD_FOUR and s<DEAD_FOUR+LIVE_THREE:
            return LIVE_THREE
        elif s>=DEAD_FOUR+LIVE_THREE and s<DEAD_FOUR*2:
            return LIVE_FOUR
        else:
            return LIVE_FOUR*2
    if s>=2*LIVE_THREE and s < DEAD_FOUR:
        return LIVE_TWO_THREE
    return s

def score(chessboard, blackscoreboard, whitescoreboard, color):
    blackScore = 0
    whiteScore = 0
    for r in range(0, LENGTH):
        for c in range(0, LENGTH):
            if chessboard[r][c] == COLOR_BLACK:
                blackScore += blackscoreboard[r][c]
            elif chessboard[r][c] == COLOR_WHITE:
                whiteScore += whitescoreboard[r][c]

    if color == COLOR_BLACK:
        return blackScore - whiteScore
    else:
        return whiteScore - blackScore

#判断周围有无棋子
def hasNeighbor(chessboard, r, c, distance, count):
    startR = r - distance
    endR = r + distance
    startC = c - distance
    endC = c + distance
    for i in range(startR, endR + 1):
        if i < 0 or i >= LENGTH: continue
        for j in range(startC, endC + 1):
            if j < 0 or j >= LENGTH: continue
            if i == r and j == c: continue
            if chessboard[i][j] != COLOR_NONE:
                count -= 1
                if count <= 0: return True
    return False

#启发式排序
def sortPos(chessboard, blackscoreboard, whitescoreboard, color):
    fives = []
    blackfours = []
    whitefours = []
    blackdeadfours = []
    whitedeadfours = []
    blacktwothrees = []
    whitetwothrees = []
    blackthrees = []
    whitethrees = []
    blacktwos = []
    whitetwos = []
    ones = []

    idx = np.where(chessboard == 0)
    idx = list(zip(idx[0], idx[1]))
    Stept = 226 - len(idx)
    distance = 2
    count = 2
    if Stept < 4:
        distance = 1
        count = 1
    for i in idx:
        r = i[0]
        c = i[1]
        if chessboard[r][c] == COLOR_NONE:

            if not hasNeighbor(chessboard, r, c, distance, count): continue

            blackScore = blackscoreboard[r][c]
            whiteSocre = whitescoreboard[r][c]
            maxScore = max(blackScore, whiteSocre)

            point = (i[0], i[1], blackScore, whiteSocre, maxScore, color)

            if blackScore >= LIVE_FIVE:
                fives.append(point)
            elif whiteSocre >= LIVE_FIVE:
                fives.append(point)
            elif blackScore >= LIVE_FOUR:
                blackfours.append(point)
            elif whiteSocre >= LIVE_FOUR:
                whitefours.append(point)
            elif blackScore >= LIVE_TWO_THREE:
                blacktwothrees.append(point)
            elif whiteSocre >= LIVE_TWO_THREE:
                whitetwothrees.append(point)
            elif blackScore >= DEAD_FOUR:
                blackdeadfours.append(point)
            elif whiteSocre >= DEAD_FOUR:
                whitedeadfours.append(point)
            elif blackScore >= LIVE_THREE:
                blackthrees.append(point)
            elif whiteSocre >= LIVE_THREE:
                whitethrees.append(point)
            elif blackScore >= LIVE_TWO:
                blacktwos.append(point)
            elif whiteSocre >= LIVE_TWO:
                whitetwos.append(point)
            else:
                ones.append(point)

    if fives: return fives

    if color == COLOR_BLACK and blackfours: return blackfours
    if color == COLOR_WHITE and whitefours: return whitefours

    if color == COLOR_BLACK and whitefours and not blackdeadfours: return whitefours
    if color == COLOR_WHITE and blackfours and not whitedeadfours: return blackfours

    fours = []
    deadfours = []
    if color == COLOR_BLACK:
        blackfours.extend(whitefours)
        fours.extend(blackfours)
        blackdeadfours.extend(whitedeadfours)
        deadfours.extend(blackdeadfours)
    else:
        whitefours.extend(blackfours)
        fours.extend(whitefours)
        whitedeadfours.extend(blackdeadfours)
        deadfours.extend(whitedeadfours)
    if fours:
        fours.extend(deadfours)
        return fours

    result = []
    if color == COLOR_BLACK:
        blacktwothrees.extend(whitetwothrees)
        result.extend(blacktwothrees)

    else:
        whitetwothrees.extend(blacktwothrees)
        result.extend(whitetwothrees)


    if whitetwothrees or blacktwothrees: return result

    result = []
    if color == COLOR_BLACK:
        result.extend(deadfours)
        result.extend(blackthrees)
        result.extend(whitethrees)
    else:
        result.extend(deadfours)
        result.extend(whitethrees)
        result.extend(blackthrees)

    if result: return result

    twos = []
    if color == COLOR_BLACK:
        blacktwos.extend(whitetwos)
        twos.extend(blacktwos)
    else:
        whitetwos.extend(blacktwos)
        twos.extend(whitetwos)

    if twos:
        dt = np.dtype(
            [('row', np.int8), ('column', np.int8), ('blackScore', np.int32), ('whiteScore', np.int32),
             ('score', np.int32), ('color', np.int8)])
        twos = np.array(twos, dtype=dt)
        twos = np.sort(twos, order='score')[::-1]
        result.extend(twos)
    else:
        result.extend(ones)

    if len(result) > LIMIT:
        return result[0:LIMIT]

    return result

#更新棋面评分
def updateScore(chessboard, blackscoreboard, whitescoreboard, point):
    radius = 4

    def update(r, c, dir):
        color = chessboard[r][c]
        if color != COLOR_WHITE:
            bs = getScore(chessboard, r, c, COLOR_BLACK, dir)
            blackscoreboard[r][c] = bs
        else:
            blackscoreboard[r][c] = 0
        if color != COLOR_BLACK:
            ws = getScore(chessboard, r, c, COLOR_WHITE, dir)
            whitescoreboard[r][c] = ws
        else:
            whitescoreboard[r][c] = 0

    for i in range(-radius, radius + 1):
        r = point[0]
        c = point[1] + i
        if c < 0: continue
        if c >= LENGTH: break
        update(r, c, 1)

    for i in range(-radius, radius + 1):
        r = point[0] + i
        c = point[1]
        if r < 0: continue
        if r >= LENGTH: break
        update(r, c, 2)

    for i in range(-radius, radius + 1):
        r = point[0] + i
        c = point[1] + i
        if r < 0 or c < 0: continue
        if r >= LENGTH or c >= LENGTH: break
        update(r, c, 3)

    for i in range(-radius, radius + 1):
        r = point[0] + i
        c = point[1] - i
        if r < 0 or c < 0: continue
        if r >= LENGTH or c >= LENGTH: break
        update(r, c, 4)

def put(chessboard, blackscoreboard, whitescoreboard, point, color):
    r = point[0]
    c = point[1]
    chessboard[r][c] = color
    updateScore(chessboard, blackscoreboard, whitescoreboard, point)

def remove(chessboard, blackscoreboard, whitescoreboard, point):
    r = point[0]
    c = point[1]
    chessboard[r][c] = COLOR_NONE
    updateScore(chessboard, blackscoreboard, whitescoreboard, point)

#minmax算法
def mm(chessboard, blackscoreboard, whitescoreboard, color, deep, alpha, beta):
    _score = score(chessboard, blackscoreboard, whitescoreboard, color)
    bestScore = _score

    if deep <= 0 or greatOrEqual(abs(_score), LIVE_FIVE):
        return bestScore

    bestScore = MIN
    if chessboard[9][13] == -1:
        pass
    _steps = sortPos(chessboard, blackscoreboard, whitescoreboard, color)

    if not _steps: return bestScore

    for s in _steps:
        point = [s[0], s[1]]
        put(chessboard, blackscoreboard, whitescoreboard, point, color)

        pScore = mm(chessboard, blackscoreboard, whitescoreboard, changeColour(color), deep - 1, -beta, -alpha)
        pScore *= -1

        remove(chessboard, blackscoreboard, whitescoreboard, point)

        if pScore > bestScore:
            bestScore = pScore
        alpha = max(alpha, bestScore)

        if great(pScore, beta):
            pointScore = MAX - 1
            return pointScore

    return bestScore

#minmax算法
def minMax(chessboard, blackscoreboard, whitescoreboard, steps, color, deep, alpha, beta):
    for i in range(len(steps)):
        step = steps[i]
        point = [step[0], step[1]]
        put(chessboard, blackscoreboard, whitescoreboard, point, color)
        pScore = mm(chessboard, blackscoreboard, whitescoreboard, changeColour(color), deep - 1, -beta, -alpha)
        pScore *= -1
        alpha = max(alpha, pScore)
        remove(chessboard, blackscoreboard, whitescoreboard, point)
        steps[i] = (point[0], point[1], pScore)

    return alpha

def deepFind(chessboard, blackscoreboard, whitescoreboard, steps, color, deep):
    bestScore = minMax(chessboard, blackscoreboard, whitescoreboard, steps, color, deep, MIN, MAX)

    # for i in steps:
    #     print(i)
    for i in steps:
        if i[2] == bestScore:
            return (i[0], i[1])

    return (steps[0][0], steps[0][1])

#算杀模块
def vct(chessboard, blackscoreboard, whitescoreboard, color, deep):

    def sort_key(e):
        return -e[2]
    def sort_abs_key(e):
        return abs(e[2])

    def find_max(color, score):
        _result = []
        fives = []
        idx = np.where(chessboard == 0)
        idx = list(zip(idx[0], idx[1]))
        for i in idx:
            r = i[0]
            c = i[1]
            # if r == 5 and c == 10:
            #     print(1111)
            p = [r,c,0]
            if blackscoreboard[r][c] >= LIVE_FIVE:
                if color == COLOR_BLACK:
                    p[2] = LIVE_FIVE
                else:
                    p[2] = -LIVE_FIVE
                fives.append(p)
            elif whitescoreboard[r][c] >= LIVE_FIVE:
                if color == COLOR_WHITE:
                    p[2] = LIVE_FIVE
                else:
                    p[2] = -LIVE_FIVE
                fives.append(p)
            else:
                if color == COLOR_BLACK:
                    p[2] = blackscoreboard[r][c]
                else:
                    p[2] = whitescoreboard[r][c]
                if p[2] >= score:
                    _result.append(p)
        if fives: return fives
        _result.sort(key=sort_key)
        return _result

    def find_min(chessboard, blackscoreboard, whitescoreboard, color, score):
        _result = []
        fives = []
        fours = []
        deadfours = []
        idx = np.where(chessboard == 0)
        idx = list(zip(idx[0], idx[1]))
        for i in idx:
            r = i[0]
            c = i[1]
            p = [r, c, 0]
            ms = 0
            es = 0
            if color == COLOR_BLACK:
                ms = blackscoreboard[r][c]
                es = whitescoreboard[r][c]
            else:
                es = blackscoreboard[r][c]
                ms = whitescoreboard[r][c]
            if ms >= LIVE_FIVE:
                p[2] = -ms
                return [p]

            if es >= LIVE_FIVE:
                p[2] = es
                fives.append(p)
                continue

            if ms >= LIVE_FOUR:
                p[2] = -ms
                fours.insert(0,p)
                continue

            if es >= LIVE_FOUR:
                p[2] = es
                fours.append(p)
                continue

            if ms >= DEAD_FOUR:
                p[2] = -ms
                deadfours.insert(0,p)
                continue

            if es >= DEAD_FOUR:
                p[2] = es
                deadfours.append(p)
                continue

            if ms>=score or es>=score:
                p[2] = ms
                _result.append(p)
        if fives: return fives
        if fours: return fours.extend(deadfours)

        _result = deadfours.extend(_result)
        if _result:
            _result.sort(key=sort_abs_key)
        return _result


    def vct_min(color, deep):
        s = score(chessboard, blackscoreboard, whitescoreboard, color)
        if s > LIVE_FIVE: return False
        if s < -LIVE_FIVE: return True
        if deep <= 1: return False
        points = find_min(chessboard, blackscoreboard, whitescoreboard, color,Min_Score)
        if not points: return False
        if points and -points[0][2] >= LIVE_FOUR: return False

        rlist = []
        for p in points:
            put(chessboard, blackscoreboard, whitescoreboard, [p[0], p[1]], color)
            r = vct_max(changeColour(color), deep-1)
            remove(chessboard, blackscoreboard, whitescoreboard, [p[0], p[1]])
            if r:
                r.insert(0,p)
                rlist.extend(r)
                continue
            else:
                return False
        result = rlist[random.randint(0,len(rlist)-1)]
        return [result]

    def vct_max(color, deep):
        if deep <= 1: return False
        points = find_max(color, Max_Score)
        if not points: return False
        if points and points[0][2] >= LIVE_FOUR: return [points[0]]
        for p in points:
            put(chessboard, blackscoreboard, whitescoreboard, [p[0],p[1]], color)

            r = vct_min(changeColour(color),deep-1)
            remove(chessboard, blackscoreboard, whitescoreboard, [p[0],p[1]])
            if r:
                if not r == True:
                    r.insert(0,p)
                    return r
                else:
                    return [p]
        return False

    if deep <= 0: return False

    Max_Score = DEAD_FOUR
    Min_Score = LIVE_FIVE

    result = vct_max(color,deep)

    if result:
        result.sort(key=sort_key)
        return result

    return False

#初始化棋面情况
def init(chessboard, blackscoreboard, whitescoreboard):
    for i in range(0, LENGTH):
        for j in range(0, LENGTH):
            if chessboard[i][j] == COLOR_BLACK:
                blackscoreboard[i][j] = getScore(chessboard, i, j, COLOR_BLACK)
                whitescoreboard[i][j] = 0
            elif chessboard[i][j] == COLOR_WHITE:
                whitescoreboard[i][j] = getScore(chessboard, i, j, COLOR_WHITE)
                blackscoreboard[i][j] = 0
            else:
                if hasNeighbor(chessboard, i, j, 2, 2):
                    blackscoreboard[i][j] = getScore(chessboard, i, j, COLOR_BLACK)
                    whitescoreboard[i][j] = getScore(chessboard, i, j, COLOR_WHITE)

if __name__ == '__main__':
    #棋盘
    chessboard = list()
    opts, args = getopt.getopt(sys.argv[1:], "r:b:")
    
    try:
        role = int(opts[0][1])
        with open(opts[1][1], 'r', encoding='utf-8') as b:
            for lines in b.readlines():
                lines = list(map(int, lines.strip().split(',')))
                chessboard.append(lines)
        chessboard = np.array(chessboard)
        # 创建AI
        a = AI(15, role, 0)
        start = time.time()
        # 开始计算下一步
        a.go(chessboard)
        # 输出结果
        print('Next Step:', a.candidate_list[-1])
        print('Cost:', time.time() - start)
    except:
        print('Error occired!')
        pass
    
    
