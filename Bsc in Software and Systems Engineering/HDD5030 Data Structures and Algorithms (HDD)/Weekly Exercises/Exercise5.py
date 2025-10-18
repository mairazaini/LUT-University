# exercise5_solution.py

from typing import List, Tuple

class PriorityQueue:
    def __init__(self):
        self._elems: List[Tuple[int, str]] = []

    def is_empty(self) -> bool:
        return not self._elems

    def push(self, item: Tuple[int, str]):
        self._elems.append(item)
        self._sift_up(len(self._elems) - 1)

    def pop(self) -> Tuple[int, str]:
        if self.is_empty():
            raise IndexError("pop from empty priority queue")
        top = self._elems[0]
        last = self._elems.pop()
        if self._elems:
            self._elems[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, idx: int):
        e = self._elems[idx]
        parent = (idx - 1) // 2
        while idx > 0 and e[0] < self._elems[parent][0]:
            self._elems[idx] = self._elems[parent]
            idx = parent
            parent = (idx - 1) // 2
        self._elems[idx] = e

    def _sift_down(self, idx: int):
        e = self._elems[idx]
        n = len(self._elems)
        child = 2 * idx + 1
        while child < n:
            if child + 1 < n and self._elems[child + 1][0] < self._elems[child][0]:
                child += 1
            if e[0] <= self._elems[child][0]:
                break
            self._elems[idx] = self._elems[child]
            idx = child
            child = 2 * idx + 1
        self._elems[idx] = e


def simulate_food_delivery():
    pq = PriorityQueue()
    orders = [
        (2, "VIP Order #101"),
        (3, "Normal Order #102"),
        (1, "Urgent Order #103"),
        (3, "Normal Order #104"),
        (2, "VIP Order #105"),
    ]

    for order in orders:
        pq.push(order)

    while not pq.is_empty():
        priority, desc = pq.pop()
        print(f"Dispatched {desc} (priority {priority})")


if __name__ == "__main__":
    simulate_food_delivery()

# AI Statement: AI tools such as VS Code Copilot were used to assist and 
# manage error in the development of this code.