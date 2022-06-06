import subprocess as sp
import pickle
import time

def cut_video(name, time, idx):
    cmd = "ffmpeg -y -ss %f -to %f -i %s -c copy %s" % (time[0], time[1], f'{name}.mp4', f'{name}_{idx}.mp4')
    p = sp.Popen(cmd, shell=True)
    p.wait()
    return p
    
    
    
def join_video(file, outname):
    cmd = f"ffmpeg -y -f concat -safe 0 -i {file} -c copy {outname}"
    p = sp.Popen(cmd, shell=True)
    return p
    
    
def main():
    name = "test"
    with open(f'{name}.pkl', 'rb') as f:
        text, time = pickle.load(f)
    
    cut_time = []
    with open('output.txt', 'r', encoding="utf_8") as f:
        for line in f:
            line = line.strip()
            print(line)
            idx = text.index(line)
            #cut_time.append((time[idx][0], time[min(idx+2, len(time)-1)][1]))
            cut_time.append(time[idx])
    
    subp = []
    idx = 0
    for time in cut_time:
        subp.append(cut_video(name, time, idx))
        idx += 1
    #idx = 5
    print('idx:', idx)
    with open('videos.txt', 'w', encoding="utf_8") as f:
        for i in range(idx):
            #f.write(f'{name}_{i}.mp4\n')
            f.write(f"file {name}_{i}.mp4\n")
    
    p = join_video('videos.txt', f'{name}_output.mp4')
    p.wait()
    
        


if __name__ == "__main__":
    main()