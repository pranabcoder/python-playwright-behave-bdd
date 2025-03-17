from playwright.sync_api import Playwright, Browser, Page


class CustomContext:
    def __init__(self, page: Page, browser: Browser, playwright: Playwright):
        self.page = page
        self.browser = browser
        self.playwright = playwright
