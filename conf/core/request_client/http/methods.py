from dataclasses import dataclass


@dataclass(frozen=True)
class HttpMethods:
    GET: str = "GET"
    HEAD: str = "HEAD"
    POST: str = "POST"
    PUT: str = "PUT"
    DELETE: str = "DELETE"
    PATCH: str = "PATCH"
    CONNECT: str = "CONNECT"
    OPTIONS: str = "OPTIONS"
    TRACE: str = "TRACE"
