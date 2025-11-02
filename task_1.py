import random
import time
from collections import OrderedDict

class LRUCach:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

def range_sum_no_cache(array, left, right):
     return sum(array[left:right + 1])

def update_no_cache(array, index, value):
    array[index] = value

cache = LRUCach(capacity=1000)  

def range_sum_with_cache(array, left, right):
    key = (left, right)
    result = cache.get(key)
    if result == -1:
        result = sum(array[left:right + 1])
        cache.put(key, result)
    return result

def update_with_cache(array, index, value):
    array[index] = value

    keys_to_delete = [key for key in cache.cache.keys() if key[0] <= index <= key[1]]
    for key in keys_to_delete:
        del cache.cache[key]

def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n // 2), random.randint(n // 2, n - 1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries

def main():
    n = 100_000
    q = 50_000
    array = [random.randint(1, 100) for _ in range(n)]
    queries = make_queries(n, q)

    arr_no_cache = array.copy()
    t1 = time.time()
    for query in queries:
        if query[0] == "Range":
            _, L, R = query
            range_sum_no_cache(arr_no_cache, L, R)
        else:
            _, idx, val = query
            update_no_cache(arr_no_cache, idx, val)
    t2 = time.time()
    no_cache_time = t2 - t1

    arr_cache = array.copy()
    t3 = time.time()
    for query in queries:
        if query[0] == "Range":
            _, L, R = query
            range_sum_with_cache(arr_cache, L, R)
        else:
            _, idx, val = query
            update_with_cache(arr_cache, idx, val)
    t4 = time.time()
    cache_time = t4 - t3

    print(f"No cache : {no_cache_time:.2f} sec")
    print(f"LRU-cache  : {cache_time:.2f} sec   (speedup x {no_cache_time / cache_time:.2f})")

if __name__ == "__main__":
    main()

