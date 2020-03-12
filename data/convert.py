import opencc

weights = {}
for line in open('essay.txt'):
  line = line.strip()
  word,weight = line.split('\t')
  weight = int(weight)
  if len(word) > 1:
    continue
  word_simp = opencc.convert(word, config='t2s.json')
  if word == word_simp:
    weights[word] = max(weight, weights.get(word, 0))
  else:
    weights[word] = max(weight, weights.get(word, 0))
    weights[word_simp] = max(weight, weights.get(word, 0))

outfile = open('../cangjie5_tradsimp.dict.yaml', 'wt')
print('''---
name: "cangjie5_tradsimp"
version: "0.18"
sort: by_weight
use_preset_vocabulary: false
max_phrase_length: 1
min_phrase_weight: 100
...
''', file=outfile)

found_start = False
for line in open('cangjie5.dict.yaml'):
  line = line.strip()
  if not found_start:
    if line == '...':
      found_start = True
    continue
  parts = line.split('\t')
  if len(parts) < 2:
    continue
  word = parts[0]
  if len(word) > 1:
    continue
  code = parts[1]
  if 'z' in code:
    continue
  weight = weights.get(word, 0)
  print(f'{word}\t{code}\t{weight}', file=outfile)
outfile.close()
