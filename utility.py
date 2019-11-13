import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

NONZERO = 1
ZERO = 0
DEDUP = 3
SPACE_THRESHOLD = 500
SEAQUEST_THRESHOLD = 5000

action_map = {"2": ["UP"], "3": ["RIGHT"], "4": ["LEFT"], "5": ["DOWN"], "6": ["UP", "RIGHT"], "7": ["UP", "LEFT"], "8": ["DOWN", "RIGHT"], "9": ["DOWN", "LEFT"], "10": ["UP"], "11": ["RIGHT"], "12": ["LEFT"], "13": ["DOWN"], "14":["UP","RIGHT"],"15":["UP","LEFT"],"16":["DOWN","RIGHT"],"17":["DOWN","LEFT"]}

action_stats = {"UP": [], "RIGHT": [], "DOWN": [], "LEFT": []}
action_time = {"UP": {}, "RIGHT": {}, "DOWN": {}, "LEFT": {}}
win_size = 500

def score_stat(path, fname):
    dirs = os.listdir(path)
    myfile = open(fname, "w+")
    myfile.write("action_id,score\n")
    for file in dirs:
        tmp = file.split("-")
        seq = tmp[0]
        score = tmp[-1].split(".")[0]
        mystr = seq + "," + score + "\n"
        myfile.write(mystr)
    myfile.close()


def get_all_score(path, games):
    for game in games:
        fname = game + ".csv"
        score_stat(os.path.join(path, game), fname)


def process_data(fname, flags):
    myfile = open(fname, "r")
    count = 0
    mylist = []
    ops = 0
    subcount = 0
    index = 0
    tmp_dict = {}
    tmp_time = {"UP": {}, "RIGHT": {}, "DOWN": {}, "LEFT": {}}
    for line in myfile:
        # ignore first five records
        if count >= 5:
            tmp = line.split("\t")
            if tmp[4] in action_map:
                index = int(count / win_size)
                tmp_list = action_map[tmp[4]]
                for i in tmp_list:
                    if index not in tmp_time[i]:
                        tmp_time[i][index] = 1
                    else:
                        tmp_time[i][index] += 1
                    if i not in tmp_dict:
                        tmp_dict[i] = 1
                    else:
                        tmp_dict[i] += 1
            action = int(tmp[4])
            if action != ops:
                if flags == NONZERO:
                    if ops != 0:
                        mylist.append([index, ops, subcount])

                else:
                    mylist.append([index, ops, subcount])
                index = count
                ops = action
                subcount = 1
            else:
                if flags == NONZERO:
                    if ops != 0:
                        subcount += 1
                else:
                    subcount += 1
        count += 1
    if ops != 0:
        mylist.append([index, ops, subcount])
    for key in tmp_dict:
        action_stats[key].append(tmp_dict[key])
    for key in tmp_time:
        for i in tmp_time[key]:
            print(i)
            if i not in action_time[key]:
                action_time[key][i] = []
                action_time[key][i].append(tmp_time[key][i])
            else:
                action_time[key][i].append(tmp_time[key][i])
    return mylist


def de_dup(data):
    new_data = {}
    for traj in data:
        new_data[traj] = []
        count = 0
        for i in range(0, len(data[traj])):
            if i == 0:
                new_data[traj].append(data[traj][i])
                count += 1
            if i > 0:
                if data[traj][i][1] == data[traj][i - 1][1]:
                    new_data[traj][count - 1][2] += data[traj][i][2]
                else:
                    new_data[traj].append(data[traj][i])
                    count += 1
    return new_data


def get_valid_score_data(path, threshold, flags):
    dirs = os.listdir(path)
    dict = {}
    data = {}
    count = 0
    for file in dirs:
        tmp = file.split("-")
        seq = tmp[0]
        score = tmp[-1].split(".")[0]
        if int(score) >= threshold:
            count += 1
            res = process_data(os.path.join(path, file), flags)
            print(seq, score, len(res))
            dict[int(seq)] = int(score)
            data[int(seq)] = res
    print(count)
    return dict, data


def get_seq(data, parts):
    all_count = {}
    for traj in data:
        traj_list = data[traj]
        length = len(traj_list)
        for i in range(0, length):
            if (i + parts <= length):
                mylist = []
                for j in range(i, i + parts):
                    mylist.append(traj_list[j][1])
                new_seq = tuple(mylist)
                if new_seq not in all_count:
                    # print(new_seq, traj)
                    all_count[new_seq] = {}
                    all_count[new_seq][traj] = 1
                else:
                    if traj not in all_count[new_seq]:
                        all_count[new_seq][traj] = 1
                    else:
                        all_count[new_seq][traj] += 1
    return all_count


def get_output(data, fname):
    filename = fname + "-seq-count.tsv"
    myfile = open(filename, "w+")
    myfile.write("sequence\tfile_included\ttotal_occur\n")
    for seq in data:
        mystr = str(seq) + "\t" + str(len(data[seq])) + "\t"
        count = 0
        for traj in data[seq]:
            count += data[seq][traj]
        mystr += str(count) + "\n"
        myfile.write(mystr)
    myfile.close()


def get_space_invader(path, game):
    dict, data = get_valid_score_data(os.path.join(path, game[1]), SPACE_THRESHOLD, NONZERO)
    new_data = de_dup(data)
    all_count = get_seq(new_data, 9)
    get_output(all_count, game[1] + "-dedup")


def get_seaquest(path, game):
    dict, data = get_valid_score_data(os.path.join(path, game[0]), SEAQUEST_THRESHOLD, NONZERO)
    new_data = de_dup(data)
    all_count = get_seq(new_data, 8)
    get_output(all_count, game[0] + "-dedup")


def Average(lst, ops):
    if len(lst) == 0:
        print(ops + "\t" + str(0) + "\t" + str(0))
        return 0
    avg = sum(lst) / 33
    print(ops + "\t" + str(len(lst)) + "\t" + str(avg))
    return avg


def avg2(lst):
    if len(lst) == 0:
        return 0
    avg = sum(lst) / len(lst)
    return avg


def combine_list():
    y = {"UP": [], "RIGHT": [], "DOWN": [], "LEFT": []}
    x = {"UP": [], "RIGHT": [], "DOWN": [], "LEFT": []}
    limit = 20
    for key in action_time:
        for ele in sorted(action_time[key].keys()):
            if ele < limit:
                y[key].append(avg2(action_time[key][ele]))
                x[key].append(int(ele * win_size))
    print(y)
    print(x)
    for key in action_time:
        plt.plot(x[key], y[key], label=key, linestyle='dashed',marker='o')
    plt.legend()
    plt.show()


def main(argv):
    path = os.path.dirname(os.path.realpath(__file__))
    game = ["seaquest", "spaceinvaders"]
    # get_all_score(path, game)
    get_space_invader(path, game)
    get_seaquest(path, game)
    combine_list()
    for key in action_stats:
        Average(action_stats[key], key)


if __name__ == "__main__":
    main(sys.argv)
