import sys
import os


def generate(files, score, data, actions):
    x = 0
    y = 0
    for i in data:
        for key in actions:          
            mystr = str(x) + "," + str(actions[key]) + "\n"
            files[key].write(mystr)
        x += 1
        if i in actions:
            actions[i] += 1

def generate_2(files, score, data, actions):
	fname = "actions/" + files + '-' + str(score) + ".txt"
	fd = open(fname, "a+")
    x = 0
    y = 0
    for i in data:         
        mystr = str(x) + "," + str(i) + "\n"
        fname.write(mystr)
    fd.close()

def main(argv):
    fn =  argv[1]
    flag = int(argv[2])
    fname  = fn.split('.')[0]
    actions = {}
    files = {}
    fd = open(fn, 'r')
    count = 0
    data = []
    score = 0
    for line in fd:
        count += 1
        tmp = line.split('\t')
        if len(tmp) >= 5 and count > 2:
            if int(tmp[4]) != 0:
                if int(tmp[4]) not in actions:
                    actions[int(tmp[4])] = 0
                    try: 
                        os.mkdir(tmp[4])
                    except:
                        pass
            data.append(int(tmp[4]))
            if(count > 5):
            	score = max(int(tmp[2]), score)
    for key in actions:
        tmpname = str(key) + "/" + fname + "-" + str(key) + "-" + str(score) + ".txt"
        files[key] = open(tmpname, "a+")
    fd.close()
    if flag == 1:
    	print("here")
    	generate(files, score, data, actions)
    else:
    	print("here")
    	generate_2(fname, score, data, actions)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv)
    else:
        sys.exit()