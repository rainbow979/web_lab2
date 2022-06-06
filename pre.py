
name = "test"

def time_s(s):
    time = 0
    s = s.split(':')
    print(s)
    time = float(s[0]) * 3600 + float(s[1]) * 60 + float(s[2][:2]) + float(s[2][-3:]) / 1000.
    return time
    

def parse_time(line):
    line = line.split(' --> ')
    start_time = time_s(line[0])
    end_time = time_s(line[1])
    return [start_time, end_time]
    
idx = 0
text = []
time = []
previous = False
with open(f'{name}.srt', 'r', encoding="utf_8") as f:
    for line in f:
        line = line.strip()
        idx += 1
        if idx % 4 == 2:
            temp = parse_time(line)
            if len(time) > 0 and temp[0] - time[-1][1] < 0.1 and "test" not in name:
                time[-1][1] = temp[1]
                previous = True
            else:
                time.append(parse_time(line))
                previous = False
            #time.append(parse_time(line))
        if idx % 4 == 3:        
            if previous:
                text[-1] = text[-1] + '，' + line
            else:
                text.append(line)
print(len(text), time[:5])
import pickle
with open(f'{name}.pkl', 'wb') as f:
    pickle.dump((text[:], time[:]), f)
    
    
text = '。'.join(text[:])
with open(f'{name}.txt', 'w') as f:
    f.write(text)
    
