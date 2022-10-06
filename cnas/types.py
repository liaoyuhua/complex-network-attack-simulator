"""
Types.
"""
from typing import Union, Tuple


NUMBER = Union[int, float]
NODE = Union[NUMBER, str]
EDGE = Tuple[NODE, NODE]