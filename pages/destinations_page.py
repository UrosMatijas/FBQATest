from playwright.sync_api import Page, expect
from urllib.parse import urljoin
import re
from utils.utils import get_all_prices, is_sorted_ascending, is_sorted_descending
from fake_env import base_url

class DestinationPage:
    CHARTER_CARD_SELECTOR = "[data-testid='single-charter-card-container']"
    TITLE_SELECTOR = "[data-testid='charter-card-title']"
    BOAT_LENGTH_SELECTOR = "[data-testid='charter-card-boat-silhouette'] div"
    MAX_PEOPLE_SELECTOR = "[data-testid='charter-card-boat-silhouette'] div + p"
    PRICE_SELECTOR = "[data-testid='charter-card-trip-from-container']"
    WISHLIST_SELECTOR = "[data-testid='add-to-wishlist']"
    WISHLIST_TOOLTIP_INFO = "Add listing to wishlist"
    SEE_AVAILABILITY_SELECTOR = "[data-testid='charter-card-see-availability-button']"
    PRICE_LOWEST_BUTTON_SELECTOR = "[data-testid='sort-price-lowest-button']"
    h1_selector = "h1"

    def __init__(self, page: Page):
        self.page = page

    @property
    def charter_cards(self):
        return self.page.locator(self.CHARTER_CARD_SELECTOR)
    
    @property
    def first_charter_card(self):
        return self.charter_cards.first

    def wait_for_charters(self, min_cards: int = 10):
        self.charter_cards.first.wait_for()
        count = self.charter_cards.count()
        assert count >= min_cards, f"Expected {min_cards} cards, found {count}"

    def assert_opened_page(self):
        h1_locator = self.page.locator(self.h1_selector)
        expect(h1_locator).to_be_visible()
        h1_pattern = r".*Fishing Charters.*"
        assert re.match(h1_pattern, h1_locator.inner_text()), "h1 does not match pattern (wrong page)"
        expect(self.first_charter_card).to_be_visible()

    def assert_first_card_info(self):
        title = self.first_charter_card.locator(self.TITLE_SELECTOR).first
        
        expect(title).to_be_visible()
        assert title.inner_text().strip(), "Empty title"

        href = title.get_attribute("href")
        assert href and href.strip(), "Empty link"

        boat_length = self.first_charter_card.locator(self.BOAT_LENGTH_SELECTOR).inner_text().strip()
        pattern = r"^\d+\s*ft$"
        assert re.match(pattern, boat_length), "Boat length is not 'number ft' format"

        max_people = self.first_charter_card.locator(self.MAX_PEOPLE_SELECTOR).inner_text().strip()
        pattern1 = r"^Up to \d+ people$"
        assert re.match(pattern1, max_people), "Max people is not good"

        price_container = self.first_charter_card.locator(self.PRICE_SELECTOR)
        expect(price_container).to_be_visible()

        price_label = price_container.locator("div").first
        expect(price_label).to_be_visible()
        
        price_text = price_label.inner_text().strip()
        assert price_text == "Trips from", "Wrong label on price"

        price_b = price_container.locator("b")
        expect(price_b).to_be_visible()
        pattern2 = r"^€\d+$"
        assert re.match(pattern2, price_b.inner_text().strip()), "Wrong format for price"

    def assert_wishlist_hover(self):
        wishlist_heart = self.first_charter_card.locator(self.WISHLIST_SELECTOR)

        wishlist_heart.hover()
        tooltip = self.page.get_by_text(self.WISHLIST_TOOLTIP_INFO)
        expect(tooltip).to_be_visible()

    def assert_see_availability_button(self):
        see_availability_button = self.first_charter_card.locator(self.SEE_AVAILABILITY_SELECTOR)
        expect(see_availability_button).to_be_visible()

        href = see_availability_button.get_attribute("href")
        assert href and href.strip(), "Button not linked"

    def assert_lowest_price_sort(self):
        self.page.locator(self.PRICE_LOWEST_BUTTON_SELECTOR).click()
        expect(self.first_charter_card).to_be_visible()
        prices = get_all_prices(self.page.locator(f"{self.PRICE_SELECTOR} b:visible"))

        assert is_sorted_ascending(prices), "Ascending sort not correct"

    def assert_highest_price_sort(self):
        sort_by_button = self.page.get_by_text("Sort by", exact=False)
        sort_by_button.click()

        highest_selector = self.page.get_by_text("(Highest)", exact=False)
        highest_selector.click()

        apply_button = self.page.get_by_text("Apply")
        apply_button.click()

        expect(self.first_charter_card).to_be_visible()

        prices = get_all_prices(self.page.locator(f"{self.PRICE_SELECTOR} b:visible"))
        assert is_sorted_descending(prices), "Descending sort not correct"

    def assert_charter_is_opened(self):
        charter_link = self.first_charter_card.locator(self.SEE_AVAILABILITY_SELECTOR)
        charter_href = charter_link.get_attribute("href")

        target_url = urljoin(base_url, charter_href)

        # BE check za response
        resp = self.page.request.get(target_url, timeout=10000)
        assert resp is not None, "No response"

        with self.page.context.expect_page() as new_page:
            charter_link.click()

        new = new_page.value
        expect(new).to_have_url(target_url)
        new.wait_for_load_state("domcontentloaded")
        new.wait_for_load_state("networkidle")
        
        charter_title = self.first_charter_card.locator(self.TITLE_SELECTOR).inner_text()
        expect(self.page.get_by_text(charter_title, exact=False)).to_be_visible()

        # moze da se proveri sta god ako znam da postoji na toj stranici recimo cena, duzina broda itd
        # moze i request response za stranicu recimo, da se ocekuje status < 400, itd