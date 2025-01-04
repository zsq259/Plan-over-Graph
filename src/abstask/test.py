import json

with open('/home/maxb/hst/test/data/abstask/result/llama-31-8b-instruct-sft11/10-3-1000-output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(len(data))

count = 0
count1 = 0
count2 = 0

for d in data:
    flag = 0
    if not d['result']:
        flag = 1
        count1 += 1
        count2 += 1
    if d['result'] and d['question']['min_time'] != d['result'][0]:
        print(d['question']['min_time'], d['result'][0])
        count1 += 1
        flag = 1
    if d['result'] and d['question']['min_cost'] != d['result'][1]:
        print(d['question']['min_cost'], d['result'][1])
        count2 += 1
        flag = 1
    count += flag
        
print(count1, count2, count)