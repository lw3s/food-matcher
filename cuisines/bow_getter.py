from enum import IntEnum

import requests


Cuisine = int


class Cuisines(IntEnum):
    MEXICAN=1
    ITALIAN=2
    GREEK=3
    INDIAN=4
    THAI=5
    CHINESE=6


def get_bow(cuisine: Cuisine) -> list[str]:
    """
    Fetch a "bag of words" from the allrecipes.com page for the input cuisine

    @param cuisine: one of the 6 cuisines laid out in Cuisines enum
    @return: a list of strings representing the important words on that cuisine's allrecipes page
    """
    ...
