import random
import math
import os
from copy import deepcopy
import time

game_size = [20, 10]
log_name = int(time.time())


def main():
    log_map = []
    first_map = create_level(game_size[0], game_size[1])
    m = deepcopy(first_map)
    base = set_base(game_size[0], game_size[1])
    # base = [0,0]
    print_level(m)
    print("base",base,sep=' ')
    while True:
        player = user_input()
        log_save(m, base, player)
        if player[0] == base[0] and player[1] == base[1]:
            print("Game over")
            break
        os.system('cls')
        if m[player[0]][player[1]] <= 0:
            print("Cnnot distroy empty sufface. Try agine")
        m = cal_map(m, player)
        m = manage_map(first_map, m)

        if m[base[0]][base[1]] == 0:
            print("Game over")
            log_save(m, base, player)
            break
        print_level_hide(m, base)
        # print_level(m)

    print("print Log")
    input("Enter to exit")

def log_save(level, base, player):
    fo = open(str(log_name)+".txt","a+")
    for i, x in enumerate(level):
        if i == 0:
            fo.write("\t")
            for k in range(0, len(x)):
                fo.write("%5d" % (k))
            fo.write("\n")
        fo.write(str(i)+"\t")
        for y in x:
            fo.write("%5d"%(y))
        fo.write("\n")
    fo.write("--------------------------------------------------\n")
    fo.write("Base@"+str(base)+" PlayerIn@"+str(player)+"\n")
    fo.close()

def create_level(x=20, y=10):
    level = list()
    for i in range(0, x+1):
        level.append(list())
        for j in range(0, y+1):
            level[i].append(random.randrange(0, 1024))
    return level


def create_level_mean(x=20, y=10):
    level = list()
    for i in range(0, x+1):
        level.append(list())
        for j in range(0, y+1):
            level[i].append(1024)
    return level


def print_level(level):
    for i, x in enumerate(level):
        if i == 0:
            print("\t",end='')
            for k in range(0, len(x)):
                print("%5d" % (k), end='')
            print()
        print(i, end="\t")
        for y in x:
            if y > 0:
                print("%5d"%(y), end='')
            else:
                print("     ", end='')
        print()


def print_level_hide(level, base):
    for i, x in enumerate(level):
        if i == 0:
            print("\t",end='')
            for k in range(0, len(x)):
                print("%5d" % (k), end='')
            print()
        print(i, end="\t")
        for j, y in enumerate(x):
            if y > 0:
                if base[0]==i and base[1] == j:
                    print("%5s" % ('BASE'), end='')
                else:
                    print("%5s"%('[K]'), end='')
            else:
                print("     ", end='')
        print()


def cal_map(array_map, player):
    new_map = array_map
    if new_map[player[0]][player[1]] <= 0:
        return new_map
    else:
        for i, x in enumerate(new_map):
            for j,y in enumerate(x):
                new_map[i][j] = cal_damage(new_map[i][j], new_map[player[0]][player[1]], player[0], player[1], i, j)
        # new_map[player[0]][player[1]] = 0
    return new_map


def manage_map(first_map, now_map):
    temp = now_map
    for i, x in enumerate(now_map):
        for j,y in enumerate(x):
            deltra = int(first_map[i][j]) - int(now_map[i][j])
            percentage = (deltra/(1+first_map[i][j]))
            if percentage > 1-0.09:
                temp[i][j] = 0
    return temp


def distance(x1, y1, x2, y2):
    return math.sqrt(((x1-x2)**2)+((y1-y2)**2))


def cal_damage(val ,destroy_val , player_pos_x, player_pos_y, ref_pos_x, ref_pos_y):
    dst = distance(player_pos_x,player_pos_y, ref_pos_x, ref_pos_y)
    #cal = val - ((destroy_val+math.fabs((((destroy_val-val)/1+val)*10)))/(1+round(dst,0)))
    cal = val - destroy_val/(1+round(dst,0))
    # print(val, player_pos_x, player_pos_y, ref_pos_x, ref_pos_y, dst, cal)
    return 0 if (cal <= 0) else cal


def set_base(size_x ,size_y):
    return [random.randrange(0,size_x+1), random.randrange(0,size_y+1)]


def user_input():
    while True:
        player = input("Pos >> ")
        player = str(player).strip().split(' ')
        player = list(filter(None, player))
        if len(player) >= 2:
            if str(player[0]).isnumeric() and str(player[1]).isnumeric():
                if (0 <= int(player[0]) <= game_size[0]) and (0 <= int(player[1]) <= game_size[1]):
                    return [int(player[0]), int(player[1])]
                else:
                    print("number not bigger than ("+str(game_size[0])+","+str(game_size[1])+")")
        print("plz input position with x <space> y")

if __name__ == '__main__':
    main()
