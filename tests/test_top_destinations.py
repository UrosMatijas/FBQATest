import pytest
from pages.sitemap_page import SitemapPage
from pages.destinations_page import DestinationPage

@pytest.fixture
def destination_page(page) -> DestinationPage:
    sitemap = SitemapPage(page)
    sitemap.goto()
    sitemap.open_some_top_destination()

    dest = DestinationPage(page)
    dest.wait_for_charters(min_cards=10)
    return dest

def test_page_can_open(destination_page: DestinationPage):
    destination_page.assert_opened_page()

def test_destination_first_card_ui(destination_page: DestinationPage):
    destination_page.assert_first_card_info()
    destination_page.assert_wishlist_hover()
    destination_page.assert_see_availability_button()

def test_sorting_by_price(destination_page: DestinationPage):
    destination_page.assert_lowest_price_sort()
    destination_page.assert_highest_price_sort()

# ovaj treba da padne
def test_charter_link(destination_page: DestinationPage):
    destination_page.assert_charter_is_opened()