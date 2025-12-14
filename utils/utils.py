import re
from typing import List
from playwright.sync_api import Locator

def get_all_prices(selector: Locator) -> List[int]:
    prices: List[int] = []
    count = selector.count()

    for i in range(count):
        ith_price = selector.nth(i)
        text = ith_price.inner_text().strip()

        match = re.search(r"(\d+)", text)
        if not match:
            raise ValueError(f"Cannot parse price from '{text}'")

        value = int(match.group(1))
        prices.append(value)

    return prices

def is_sorted_ascending(numbers_list: List[int]) -> bool:
    return numbers_list == sorted(numbers_list)

def is_sorted_descending(numbers_list: List[int]) -> bool:
    return numbers_list == sorted(numbers_list, reverse=True)