from playwright.sync_api import sync_playwright
from utils.CustomContext import CustomContext
import json
from utils.logger_config import logger
import allure
from allure_commons.types import AttachmentType
from pages.BasePage import BasePage


def before_all(context):
    # This function is called before all tests start
    logger.info("Starting Playwright....")

    # Load environment variables from env.json
    with open('config/env.json', 'r') as file:
        env_vars = json.load(file)

    # Accessing variables from env.json
    browser_type = env_vars["browser"]
    headless_mode = env_vars["headless"]
    contact_us_url = env_vars["base_url"]

    playwright = sync_playwright().start()
    browser = playwright[browser_type].launch(headless=headless_mode, args=["--start-maximized"])
    page = browser.new_page(no_viewport=True)

    # Initialize CustomContext
    context.custom_context = CustomContext(page, browser, playwright)
    context.contact_us_url = contact_us_url


def before_scenario(context, scenario):
    # This function is called before each scenario
    logger.info(f"Starting Scenario: {scenario.name}")
    if not hasattr(context.custom_context, 'page') or context.custom_context.page.is_closed():
        context.custom_context.page = context.custom_context.browser.new_page(
            no_viewport=True)  # Create a new page if it doesn't exist or is closed
    context.base_page = BasePage(context.custom_context)


def after_scenario(context, scenario):
    # This function is called after each scenario
    # Capture screenshot
    screenshot_path = f"screenshots/{scenario.name.replace(' ', '_')}.png"
    context.custom_context.page.screenshot(path=screenshot_path)
    logger.info(f"Captured screenshot for failed Scenario: {screenshot_path}")

    # Attach screenshot to Allure report
    with open(screenshot_path, "rb") as image_file:
        allure.attach(image_file.read(), name=scenario.name, attachment_type=AttachmentType.PNG)

    logger.info(f"Ending Scenario: {scenario.name}")
    context.custom_context.page.close()


def after_all(context):
    # This function is called after all tests have finished
    logger.info("Stopping Playwright....")
    context.custom_context.browser.close()  # Close the browser
    context.custom_context.playwright.stop()  # Stop the Playwright instance
