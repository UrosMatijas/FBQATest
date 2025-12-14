from playwright.sync_api import Page
from fake_env import base_url

BASE_URL = f"{base_url}/sitemap"

class SitemapPage:
    TOP_DESTINATIONS_HEADING_SELECTOR = "h1:has-text('Top Fishing Destinations') + div"
    DESTINATION_LINKS_SELECTOR = "ul li a"

    def __init__(self, page: Page, url: str = BASE_URL):
        self.page = page
        self.url = url

    def goto(self):
        self.page.goto(self.url)

    def open_some_top_destination(self):
        container = self.page.locator(self.TOP_DESTINATIONS_HEADING_SELECTOR)
        container.first.wait_for()

        links = container.locator(self.DESTINATION_LINKS_SELECTOR)
        count = links.count()
        assert count > 0, "No destinations found"

        links.first.click()