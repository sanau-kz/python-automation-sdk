class Test:
    def __init__(self, text):
        self._text = text
        self.print_status()

    def change_text(self, text):
        self._text = text
        self.print_status()

    def print_status(self):
        print(f'Объект с текстом "{self._text}" успешно создан!')