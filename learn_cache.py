#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import time
from my_lrucache import LRUCacheDict
# from functools import lru_cache   #py3 lru_cache 已经是标准库

CACHE = {}

def cache_it(max_size=1024, expiration=60):
    CACHE = LRUCacheDict(max_size=max_size, expiration=expiration)
    def wrapper(func):
        def inner(*args, **kwargs):
            key = repr(*args, **kwargs)
            try:
                result = CACHE[key]
            except KeyError:
                result = func(*args, **kwargs)
                CACHE[key] = result
            return result
        return inner
    return wrapper

@cache_it(max_size=10, expiration=3)
def query(sql):
    time.sleep(1)
    result = 'execute %s'%sql
    return result


if __name__ == "__main__":
    start = time.time()
    query('select * from blog_post')
    print(time.time()-start)

    start = time.time()
    query('select * from blog_post')
    print(time.time()-start)

