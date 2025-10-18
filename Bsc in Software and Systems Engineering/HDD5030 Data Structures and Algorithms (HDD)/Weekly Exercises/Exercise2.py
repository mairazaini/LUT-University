# Exercise 2

# 1: Detect Duplicates with Recursion
def has_duplicate(lst):
    if len(lst) <= 1:
        return False
    if lst[0] in lst[1:]:
        return True
    return has_duplicate(lst[1:])

def has_duplicate_set(lst, seen=None):
    if seen is None:
        seen = set()
    if not lst:
        return False
    if lst[0] in seen:
        return True
    seen.add(lst[0])
    return has_duplicate_set(lst[1:], seen)

# 2: Implement a Sequential List
class SequentialList:
    def __init__(self, capacity=10):
        self.data = [None] * capacity
        self.length = 0
        self.capacity = capacity

    def is_empty(self):
        return self.length == 0

    def size(self):
        return self.length

    def insert(self, index, value):
        if self.length >= self.capacity:
            raise Exception("List is full")
        if index < 0 or index > self.length:
            raise IndexError("Index out of range")
        for i in range(self.length, index, -1):
            self.data[i] = self.data[i - 1]
        self.data[index] = value
        self.length += 1

    def append(self, value):
        self.insert(self.length, value)

    def prepend(self, value):
        self.insert(0, value)

    def delete(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        removed = self.data[index]
        for i in range(index, self.length - 1):
            self.data[i] = self.data[i + 1]
        self.data[self.length - 1] = None
        self.length -= 1
        return removed

    def delete_by_value(self, value):
        index = self.find(value)
        if index != -1:
            self.delete(index)

    def delete_head(self):
        return self.delete(0)

    def delete_tail(self):
        return self.delete(self.length - 1)

    def get(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        return self.data[index]

    def update(self, index, value):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        self.data[index] = value

    def find(self, value):
        for i in range(self.length):
            if self.data[i] == value:
                return i
        return -1

    def display(self):
        print([self.data[i] for i in range(self.length)])

    def reverse(self):
        left, right = 0, self.length - 1
        while left < right:
            self.data[left], self.data[right] = self.data[right], self.data[left]
            left += 1
            right -= 1

    def clear(self):
        self.data = [None] * self.capacity
        self.length = 0

# Example
if __name__ == "__main__":
    # Testing 1
    print("Duplicate check (normal):", has_duplicate(["a", "b", "c", "a"]))
    print("Duplicate check (set):", has_duplicate_set(["x", "y", "z", "y"]))

    # Testing 2
    sl = SequentialList(5)
    sl.append(10)
    sl.append(20)
    sl.prepend(5)
    sl.insert(1, 15)
    sl.display()   # [5, 15, 10, 20]
    sl.reverse()
    sl.display()   # [20, 10, 15, 5]
