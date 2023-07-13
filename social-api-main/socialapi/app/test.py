from utils.collect_util import CollectUtil
import asyncio

collect_util = CollectUtil()


async def fun():
    await collect_util.collect_data()
    await collect_util.collect_data()
    await collect_util.collect_data()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(fun())
loop.close()
