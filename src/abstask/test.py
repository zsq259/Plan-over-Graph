import json

with open('/home/zhangsq/1/test/data/abstask/dev/10-1-100.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for d in data:
    for idx, rule in enumerate(d['question']['rules'], start=0):
        new_rule = {'id': idx}
        new_rule.update(rule)
        d['question']['rules'][idx] = new_rule

with open('/home/zhangsq/1/test/data/abstask/dev/10-1-100_copy.json.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)