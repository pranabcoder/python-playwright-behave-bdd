from playwright.sync_api import sync_playwright
from utils.CustomContext import CustomContext
import json
from utils.logger_config import logger
import allure
from allure_commons.types import AttachmentType
from pages.BasePage import BasePage
import os


def before_all(context):
    logger.info("Starting Playwright....")
    try:
        with open('config/env.json', 'r') as file:
            env_vars = json.load(file)

        browser_type = env_vars["browser"]
        headless_mode = env_vars["headless"]
        contact_us_url = env_vars["base_url"]

        playwright = sync_playwright().start()
        browser = playwright[browser_type].launch(headless=headless_mode, args=["--start-maximized"])
        page = browser.new_page(no_viewport=True)

        context.custom_context = CustomContext(page, browser, playwright)
        context.contact_us_url = contact_us_url
    except Exception as e:
        logger.error(f"Error in before_all: {e}")
        raise


def before_scenario(context, scenario):
    logger.info(f"Starting Scenario: {scenario.name}")
    try:
        if not hasattr(context.custom_context, 'page') or context.custom_context.page.is_closed():
            context.custom_context.page = context.custom_context.browser.new_page(no_viewport=True)
        context.base_page = BasePage(context.custom_context)
    except Exception as e:
        logger.error(f"Error in before_scenario: {e}")
        raise


def after_scenario(context, scenario):
    try:
        screenshot_path = f"screenshots/{scenario.name.replace(' ', '_')}.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        context.custom_context.page.screenshot(path=screenshot_path)
        logger.info(f"Captured screenshot for Scenario: {screenshot_path}")

        with open(screenshot_path, "rb") as image_file:
            allure.attach(image_file.read(), name=scenario.name, attachment_type=AttachmentType.PNG)

        logger.info(f"Ending Scenario: {scenario.name}")
        context.custom_context.page.close()
    except Exception as e:
        logger.error(f"Error in after_scenario: {e}")
        raise


def after_all(context):
    logger.info("Stopping Playwright....")
    try:
        context.custom_context.browser.close()
        context.custom_context.playwright.stop()
    except Exception as e:
        logger.error(f"Error in after_all: {e}")
        raise
