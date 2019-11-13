import numpy as np
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join

SEAQ_DATA_DIR = "seaquest_actions/"
SPACE_DATA_DIR = "spaceinvaders_actions/"
SAVE_FOLDER_FIR = "./TRAJ_VIZ"

def read_data(directory, filename_list):
    traj_list = []
    score_list = []
    score_dict = {}
    max_len = 0
    count = 0
    for f in filename_list:
        score_id = f.split('.')[0].split('-')[0]+"_"+f.split('.')[0].split('-')[-1]
        score_list.append(score_id)
        traj = np.loadtxt(join(directory, f), delimiter=',')
        max_len = max(max_len,len(traj))
        traj_list.append(traj)
        if score_id  not in score_dict:
            score_dict[score_id] = count
            count += 1
    # print(traj_list)
    return traj_list, score_list, max_len, score_dict

def read_xy(traj_list):
    x = [list(i[0] for i in traj_list[j]) for j in range(len(traj_list))]
    y = [list(i[1] for i in traj_list[j]) for j in range(len(traj_list))]
    # print(x)
    # print(y)
    return x, y

def plot(x, y, score_list, game_name,max_len,score_dict):
    color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    mydict = {"0":"NOOP","1":"FIRE","2":"UP","3":"RIGHT","4":"LEFT","5":"DOWN","6":"UPRIGHT","7":"UPLEFT","8":"DOWNRIGHT","9":"DOWNLEFT","10":"UPFIRE","11":"RIGHTFIRE","12":"LEFTFIRE","13":"DOWNFIRE","14":"UPRIGHTFIRE","15":"UPLEFTFIRE","16":"DOWNRIGHTFIRE","17":"DOWNLEFTFIRE"}
    styles = ["default","steps-pre","steps-mid", "steps-post"]
    style = "steps-pre"
    working_folder = '{}/{}'.format(SAVE_FOLDER_FIR, game_name)
    if not os.path.exists(working_folder):
        os.makedirs(working_folder)
    # fig, axes = plt.subplots(nrows=len(styles), figsize=(4,7))
    # for ax, style in zip(axes, styles):
    #     ax.plot(x,y, drawstyle=style)
    #     ax.set_title("drawstyle={}".format(style))
    mylist = []

    fig, ax = plt.subplots(len(score_dict), 1, sharey='row', figsize=(16,16))
    for idx in range(len(x)):
        x_tmp = x[idx]
        y_tmp = y[idx]
        # ax = plt.figure(figsize=(16,10))
        # plt.plot(x_tmp, y_tmp)
        # plt.title("Action:" + action_dir)
        # plt.legend()
        index = score_dict[score_list[idx]]
        color_tmp = color[index % len(score_dict)]
        print(index)
        ax[index].plot(x_tmp, y_tmp, drawstyle=style, label=score_list[idx], alpha=0.7, linewidth=0.5, color=color_tmp)
        ax[index].legend(title="playerID_score")
        # ax[index].scatter(x_tmp, y_tmp, label=score_list[idx], alpha=0.7)
    fig.suptitle("Action Timeline of {}".format(game_name))
    
    plt.savefig('{}/{}/action_timeline.png'.format(SAVE_FOLDER_FIR, game_name), bbox_inches='tight')
    # ax.set_title("drawstyle={}".format(style))
    # fig.tight_layout()
    # plt.show()
    
    

def main():
    seaquest = True
    space = True
    if seaquest:
        seaq_file_list = [f for f in listdir(SEAQ_DATA_DIR) if f.lower().endswith(('.txt'))]
        print(seaq_file_list)
        seaq_traj_list, score_list, max_len, score_dict = read_data(SEAQ_DATA_DIR, seaq_file_list)
        print(score_list)
        seaq_x, seaq_y = read_xy(seaq_traj_list)
        plot(seaq_x, seaq_y, score_list, "seaquest", max_len, score_dict)
    if space:
        space_file_list = [f for f in listdir(SPACE_DATA_DIR) if f.lower().endswith(('.txt'))]
        print(space_file_list)
        space_traj_list, score_list,max_len, score_dict = read_data(SPACE_DATA_DIR, space_file_list)
        print(score_list)
        space_x, space_y = read_xy(space_traj_list)
        plot(space_x, space_y, score_list, "spaceinvaders",max_len, score_dict)

if __name__ == "__main__":
    main()