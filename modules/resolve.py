import asyncio
import aiodns

from config import settings
from config.log import logger


class Resolve(object):
    def __init__(self, domains: list) -> None:
        self.domains = domains
        self.datas = dict()
        self.queue = asyncio.Queue()
        self.resolver = None

    async def query(self, name: str, query_type: str):
        return await self.resolver.query(name, query_type)

    async def __worker(self) -> None:
        while not self.queue.empty():
            domain = await self.queue.get()
            try:
                answers = await self.query(domain, "A")
                tmp = list()
                for itm in answers:
                    try:
                        tmp.append(itm.host)
                    except Exception as identifier:
                        logger.log("DEBUG", f"{domain}: {repr(identifier)}")
                self.datas[domain] = list(set(tmp))
                logger.log("INFOR", f"{domain}: {', '.join(self.datas[domain])}")
            except Exception as identifier:
                logger.log("ALERT", f"{domain}: {repr(identifier)}")
            self.queue.task_done()

    async def __arrang_task(self) -> None:
        for domain in self.domains:
            await self.queue.put(domain)
        tasks = [self.__worker() for i in range(settings.async_semaphore)]
        await asyncio.wait(tasks)

    def run(self) -> dict:
        try:
            logger.log("INFOR", "Start resolve domain IP")
            logger.log("INFOR", "May take a while")
            loop = asyncio.get_event_loop()
            self.resolver = aiodns.DNSResolver(loop=loop)
            loop.run_until_complete(self.__arrang_task())
            loop.close()
            logger.log("INFOR", "Finished resolve domain IP")
        except Exception as identifier:
            logger.log("ERROR", repr(identifier))
        return self.datas
