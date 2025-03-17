from pages.BasePage import BasePage


class ContactUsPage(BasePage):
    def __init__(self, context):
        super().__init__(context)
        self._first_name_field = '[name="first_name"]'
        self._last_name_field = '[name="last_name"]'
        self._email_field = '[name="email"]'
        self._message_field = '[name="message"]'
        self._submit_button = '[value="SUBMIT"]'
        self._reset_button = '[value="RESET"]'

    def fill_first_name(self, first_name: str):
        self.page.fill(self._first_name_field, first_name)

    def fill_last_name(self, last_name: str):
        self.page.fill(self._last_name_field, last_name)

    def fill_email(self, email: str):
        self.page.fill(self._email_field, email)

    def fill_message(self, message: str):
        self.page.fill(self._message_field, message)

    def click_submit(self):
        self.page.click(self._submit_button)

    def click_reset(self):
        self.page.click(self._reset_button)

    def get_field_value(self, field: str):
        field_selector = self._get_field_selector(field)
        return self.page.locator(field_selector).input_value()

    def _get_field_selector(self, field: str) -> str:
        if field == "first_name":
            return self._first_name_field
        elif field == "last_name":
            return self._last_name_field
        elif field == "email":
            return self._email_field
        elif field == "message":
            return self._message_field
        else:
            raise ValueError(f"Unknown field: {field}")
