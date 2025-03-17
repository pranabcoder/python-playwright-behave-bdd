from behave import given, when, then
from pages.ContactUsPage import ContactUsPage
from utils.logger_config import logger
from playwright.sync_api import TimeoutError


@given('I am on the Contact Us form')
def navigate_to_contact_us_form(context):
    context.contact_us_page = ContactUsPage(context.base_page)
    context.contact_us_page.navigate(context.contact_us_url)


@when('I fill in the "{field}" field with "{value}"')
def fill_in_field(context, field, value):
    if value == "\\n":
        logger.info(f"Skipping field {field} as indicated by '\\n'.")
        return

    if field == "first_name":
        context.contact_us_page.fill_first_name(value)
    elif field == "last_name":
        context.contact_us_page.fill_last_name(value)
    elif field == "email":
        context.contact_us_page.fill_email(value)
    elif field == "message":
        context.contact_us_page.fill_message(value)
    logger.info(f"Filled field {field} with data {value}")


@when('I click on the "{button}" button')
def click_button(context, button):
    if button == "SUBMIT":
        context.contact_us_page.click_submit()
    elif button == "RESET":
        context.contact_us_page.click_reset()


@then('I should see the success message saying "{message}"')
def verify_success_message(context, message):
    success_message_selector = f'//*[contains(text(), "{message}")]'
    try:
        logger.info(f"Waiting for success message: {message}")
        context.page.wait_for_selector(success_message_selector, timeout=2000)
        assert context.page.is_visible(success_message_selector)
        logger.info(f"Success Message: {message} is visible!")
    except TimeoutError:
        logger.error(f"Success Message: {message} not found!!")
        assert False, f"Success message '{message}' not found on the page"


@then('I should see an error message saying "{message}"')
def verify_error_message(context, message):
    error_message_selector = f'//body[contains(., "{message}")]'
    try:
        logger.info(f"Waiting for error message: {message}")
        context.page.wait_for_selector(error_message_selector, timeout=2000)
        assert context.page.is_visible(error_message_selector)
        logger.info(f"Error Message: {message} is visible!")
    except TimeoutError:
        logger.error(f"Error Message: {message} not found!!")
        assert False, f"Error message '{message}' not found on the page"


@then('all fields should be cleared')
def verify_all_fields_cleared(context):
    fields = ["first_name", "last_name", "email", "message"]
    for field in fields:
        field_value = context.contact_us_page.get_field_value(field)
        assert field_value == "", f"Field {field} is not cleared"
    logger.info("All fields are cleared!")


@then('I should see the message "{expected_message}"')
def verify_message(context, expected_message):
    message_selector = f'//*[contains(text(), "{expected_message}")] | //body[contains(., "{expected_message}")]'
    try:
        logger.info(f"Waiting for message: {expected_message}")
        context.page.wait_for_selector(message_selector, timeout=2000)
        assert context.page.is_visible(message_selector)
        logger.info(f"Message: {expected_message} is visible!")
    except TimeoutError:
        logger.error(f"Message: {expected_message} not found!!")
        assert False, f"Message '{expected_message}' not found on the page"
