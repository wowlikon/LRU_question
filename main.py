import re, csv, os.path, datetime

CSV_STORAGE = "./books.csv"

def check_input(input_string):
    pattern = r'^\d{9}[\dX]$'
    if re.match(pattern, input_string):
        check_summ = 0
        for c in v[:-1]: check_summ += int(c)

        check_summ %= 11
        if check_summ == 10: check_summ = "X"
        else: check_summ = str(check_summ)
        return v[-1].upper() == check_summ
    else: return False

def dirrect_insert(fname: str, key: str, value: int):
    if not os.path.isfile(fname):
        with open(fname, 'w+'): ...
    with open(fname, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[key, value]])

def dirrect_get(fname: str, key: str) -> int:
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            for l in csv.reader(f):
                if len(l) == 0: continue
                if l[0] == key: return int(l[1])
            return -1
    else: return -1

def dirrect_remove(fname: str, key: str) -> int:
    if os.path.isfile(fname):
        val = -1

        with open(fname, 'r') as f:
            reader = csv.reader(f)
            content = list(reader)

        for i, l in enumerate(content):
            if l[0] == key:
                val = l[1]
                del content[i]

        with open(fname, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(content)

        return val
    else: return -1
        
class LRU:
    def __init__(self, N: int, csv_fname: str):
        self.N = N
        self.TimeList = {}
        self.HashTable = {}
        self.csv = csv_fname

    def __str__(self) -> str:
        groups = []
        for k, e in self.HashTable.items():
            try: t = self.TimeList[k]
            except: t = None
            groups.append(str((k, e, t)))
        return f"[{self.csv}|{self.N}]\n{'\n'.join(groups)}"
    
    def _update_key(self, key: str):
        self.TimeList[key] = datetime.datetime.now()

    def _update_cache(self, key: str):
         self._update_key(key)
         if len(self.HashTable) > self.N:
            oldest = min(self.TimeList, key=self.TimeList.get)
            if oldest in self.TimeList: self.TimeList.pop(oldest)
            if oldest in self.HashTable: self.HashTable.pop(oldest)

    def insert(self, key: str, value: int):
        if self.get(key) != -1: return
        dirrect_insert(self.csv, key, value)
        self.HashTable[key] = value
        self._update_cache(key)
      
    def get(self, key: str) -> int:
        v = self.HashTable.get(key, -1)
        if v == -1: v = dirrect_get(self.csv, key)

        if v != -1:
            self.HashTable[key] = v
            self._update_cache(key)
        self._update_key(key)
        return v
         
    def remove(self, key: str) -> int:
        # if self.get(key) != -1: return -1
        if key in self.TimeList: self.TimeList.pop(key)
        if key in self.HashTable: self.HashTable.pop(key)
        return dirrect_remove(self.csv, key)

def input_int(*args, **kwargs) -> int:
    while True:
        v = input(*args, **kwargs)
        if v.isdigit(): return int(v)
        print("Invalid value")

books = LRU(3, CSV_STORAGE)

while True:
    v = input("value: ")
    if not v: exit()
    if not check_input(v): 
        print("Invalid value")
        continue
    
    print(books)
    print("1. add new")
    print("2. get value")
    print("3. remove book")
    print("0. exit")

    a = input_int("action: ")
    if a == 0: exit()
    elif a == 1:
        print("ACTION ADD")
        while True:
            price = input_int("price: ")
            if price >= -1: break
            print("Must be positive! (-1 for cancel)")
        if price == -1:
            print("add canceled")
            continue

        books.insert(v, price)
        print()

    elif a == 2:
        print("ACTION GET")
        price = books.get(v)
        if price == -1:
            print("Book not found. Error 404")
            continue

        print(f"{v} price is {price}")
        print()

    elif a == 3:
        print("ACTION REMOVE")
        price = books.remove(v)
        if price == -1:
            print("Book not found. Error 404")
            continue

        print(f"{v} was removed. Price was {price}")
        print()

    else: print("Invalid action")
