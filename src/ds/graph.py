from typing import TypedDict, List


class IGraphLink(TypedDict):
    source: str
    target: List[str]


class IGraphData(TypedDict):
    nodes: List[dict]
    links: List[IGraphLink]
