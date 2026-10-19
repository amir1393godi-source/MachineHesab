from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window


class CalculatorApp(App):
    def build(self):
        self.title = "ماشین حساب"
        self.first_number = None
        self.operation = None
        self.start_new_number = True

        root = BoxLayout(orientation="vertical", padding=12, spacing=10)
        self.display = Label(
            text="0",
            font_size="42sp",
            halign="right",
            valign="middle",
            size_hint_y=0.28,
        )
        self.display.bind(size=self._update_text_size)
        root.add_widget(self.display)

        grid = GridLayout(cols=4, spacing=7)
        keys = [
            "C", "⌫", "÷", "×",
            "7", "8", "9", "-",
            "4", "5", "6", "+",
            "1", "2", "3", "=",
            "±", "0", ".",
        ]
        for key in keys:
            button = Button(text=key, font_size="25sp")
            button.bind(on_press=self.press)
            grid.add_widget(button)
        root.add_widget(grid)
        return root

    def _update_text_size(self, *_):
        self.display.text_size = self.display.size

    def press(self, button):
        key = button.text
        current = self.display.text

        if key == "C":
            self.display.text = "0"
            self.first_number = None
            self.operation = None
            self.start_new_number = True
            return

        if key == "⌫":
            if self.start_new_number or current == "خطا":
                self.display.text = "0"
            else:
                self.display.text = current[:-1] or "0"
            return

        if key == "±":
            if current not in ("0", "خطا"):
                self.display.text = current[1:] if current.startswith("-") else "-" + current
            return

        if key == ".":
            if self.start_new_number or current == "خطا":
                self.display.text = "0."
                self.start_new_number = False
            elif "." not in current:
                self.display.text += "."
            return

        if key.isdigit():
            if self.start_new_number or current == "0" or current == "خطا":
                self.display.text = key
            else:
                self.display.text += key
            self.start_new_number = False
            return

        if key in ("+", "-", "×", "÷"):
            try:
                self.first_number = float(current)
            except ValueError:
                self.display.text = "خطا"
                return
            self.operation = key
            self.start_new_number = True
            return

        if key == "=":
            if self.first_number is None or self.operation is None:
                return
            try:
                second_number = float(current)
                if self.operation == "+":
                    result = self.first_number + second_number
                elif self.operation == "-":
                    result = self.first_number - second_number
                elif self.operation == "×":
                    result = self.first_number * second_number
                else:
                    if second_number == 0:
                        self.display.text = "تقسیم بر صفر!"
                        self.first_number = None
                        self.operation = None
                        self.start_new_number = True
                        return
                    result = self.first_number / second_number
                if result.is_integer():
                    self.display.text = str(int(result))
                else:
                    self.display.text = str(round(result, 8))
                self.first_number = None
                self.operation = None
                self.start_new_number = True
            except (ValueError, OverflowError):
                self.display.text = "خطا"
                self.first_number = None
                self.operation = None
                self.start_new_number = True


if __name__ == "__main__":
    CalculatorApp().run()
