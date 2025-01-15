import time
import asyncio
import copy
async def inner(a):
    for item in range(a):
        yield item*2, item+2
        await asyncio.sleep(1)

async def outer(a):
    result = []
    async for i, j in inner(a):
        print(i,j)
        result.append((i,j))
    return result

async def outer1():
    for i in range(3):
        result = await outer(i)
        yield i, result

async def out2():
    result = outer1()
    return result

async def main():
    result = await out2()
    async for num,  item in result:
        for i,j in item:
            print(num, i, j)

asyncio.run(main())