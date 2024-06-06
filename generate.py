import sys

summ = 0
v = sys.argv[1]
for c in v: summ += int(c)

summ %= 11
if summ == 10: summ = "X"
else: summ = str(summ)
print(len(v)+1, v+summ)