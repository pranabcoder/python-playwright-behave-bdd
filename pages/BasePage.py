from utils.CustomContext import CustomContext

class BasePage:
    def __init__(self, context: CustomContext):
        self.page = context.page

    def navigate(self, url: str):
        self.page.goto(url)
