import math
log2table = {}
for i in range(1, 20):
    log2table[i] = math.log2(i)
print(log2table)

log2table = {i:math.log2(i) for i in range(1,20)}
print(log2table)
