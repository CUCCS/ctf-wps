import itertools
seed = ''

for i in range(ord('a'), ord('z') + 1):
    seed += chr(i)

for i in range(ord('A'), ord('Z') + 1):
    seed += chr(i)

for i in range(0, 10):
    seed += str(i)

res = itertools.product(seed, repeat=3) 
for i in res: 
    print('1234567' + ''.join(i))
