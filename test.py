class Test:
    max: int = 0
    curr: int = -1
    def __init__(self,max):
        self.max = max
    def __iter__(self):
        return self
    def __next__(self):
        if self.curr >= self.max:
            raise StopIteration
        self.curr += 1
        return self.curr
for x in Test(5):
    print(x)