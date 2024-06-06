import sys

#Вычисление суммы
summ = 0
v = sys.argv[1]
for c in v: summ += int(c)

#Нахождение контрольного символа
summ %= 11
if summ == 10: summ = "X"
else: summ = str(summ)
print(f"[{len(v)+1}] {v+summ}")
