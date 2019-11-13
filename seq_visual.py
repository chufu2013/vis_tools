import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

n = 2
number_of_frames = 6
# data = np.random.rand(n, number_of_frames)
f = open("combine_seq_spaceinvader", "r")
seq = {}
seq_count = []
for line in f:
    tmp = line.strip().split("\t")
    if tmp[3] not in seq:
        seq_count.append(tmp[3])
        seq[tmp[3]] = {}
        seq[tmp[3]]["x"] = []
        seq[tmp[3]]["y"] = []
        seq[tmp[3]]["z"] = []
    seq[tmp[3]]["x"].append(tmp[0])
    # file count
    seq[tmp[3]]["y"].append(int(tmp[1]))
    # occurrence
    seq[tmp[3]]["z"].append(int(tmp[2]))
f.close()
print(seq)


def subcategorybar(num, width=0.8):
    plt.clf()
    # plt.xticks([], [])
    X = seq[seq_count[num]]["x"]
    n = 2
    bar_label = ["traj_included", "total_occur"]
    vals = [seq[seq_count[num]]["y"], seq[seq_count[num]]["z"]]
    _X = np.arange(len(X))
    for i in range(n):
        plt.barh((_X - width / 2. + i / float(n) * width), vals[i], width / float(n), align="center", label=bar_label[i])
    plt.yticks(_X, X)
    plt.legend()
    plt.title("Top 10 Sequences With " + seq_count[num] + " Actions Included")
    plt.tight_layout()


# def update_hist(num, data):
#     plt.cla()
#     plt.hist(data[num])
#
fig = plt.figure(figsize=(10,5))
# hist = plt.hist(data[0])
#
animation = animation.FuncAnimation(fig, subcategorybar, number_of_frames, interval=1000, repeat=False)
# plt.show()
animation.save('animation.gif', writer='imagemagick', fps=0.5)
