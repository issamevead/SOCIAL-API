from enum import Enum, unique
from copy import deepcopy
from random import randint, shuffle
import asyncio
from typing import Any, Optional, List, Generator, Tuple
from gufo.ping import Ping
from pydantic import BaseModel

from src.log.logger import Logs


log = Logs()

unsecure_proxies = (
    "101.3",
    "101.6",
    "101.7",
    "101.8",
    "100.6",
    "100.7",
)
secure_proxies = (
    "1.1",
    "1.2",
    "1.3",
    "1.4",
    "1.5",
    "1.6",
    "1.7",
    "1.8",
    "1.9",
    "3.1",
    "3.2",
    "3.3",
    "3.5",
    "4.1",
    "4.2",
    "4.3",
    "4.4",
    "4.6",
    "78.48",
)


@unique
class Protocol(str, Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS5 = "socks5"
    SOCKS4 = "socks4"

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f'{value} is not a valid {cls.__name__}. Valid \
                types: {", ".join([str((repr(m.name), repr(m.value))) for m in cls])}'
        )


class Proxy(BaseModel):
    protocol: Protocol
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        use_enum_values = True

    def __repr__(self):
        return f"{self.host}:{self.port}"

    def __str__(self):
        return f"{self.host}:{self.port}"

    def __eq__(self, other: Any) -> bool:
        return self.__dict__ == other.__dict__

    def to_dict(self):
        return {
            "http": f"{self.protocol}://{self.host}:{self.port}",
            "https": f"{self.protocol}://{self.host}:{self.port}",
        }

    async def ping(self):
        """Check proxy"""
        ping = Ping(size=64, timeout=1.0)
        try:
            async for rtt in ping.iter_rtt(self.host, count=2):
                if rtt is None:
                    log.info(f"{self.host}:{self.port} is down, {rtt}")
                    return False
            return True
        except Exception as _:
            return False


secure_proxies = [Proxy(protocol="socks5", host=f"10.10.{p}", port=8081) for p in secure_proxies]

unsecure_proxies = [
    Proxy(protocol="socks5", host=f"10.10.{p}", port=8081) for p in unsecure_proxies
]


class Proxies:

    @staticmethod
    def proxies(proxy: Proxy = None, proxies: List[Proxy] = None) -> Tuple[Proxy, List[Proxy]]:
        if proxies is None:
            proxies = secure_proxies
        if proxy is None:
            return proxies[randint(0, len(proxies) - 1)], proxies
        proxies = deepcopy(proxies)
        if proxy in proxies:
            proxies.remove(proxy)
        return proxies[randint(0, len(proxies) - 1)], proxies

    @staticmethod
    def rand_proxy(secure: bool = False) -> Generator[Proxy, None, None]:
        """
        Return a generator of random proxies

        args:
            secure: bool, default False - if True, return only secure proxies

        returns:
            Generator[Proxy, None, None]: a generator of pingable random proxies
        """
        if secure is False:
            proxies = deepcopy(unsecure_proxies)
        else:
            proxies = deepcopy(secure_proxies)
        shuffle(proxies)
        for proxy in proxies:
            if asyncio.run(proxy.ping()) is False:
                continue
            yield proxy

    @staticmethod
    def get_proxy() -> Generator[Proxy, None, None]:
        """Return proxy"""
        for proxy in secure_proxies:
            yield proxy


Proxies.rand_proxy()