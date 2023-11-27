"""
Genderswapping application
"""
import traceback
from pathlib import Path

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, LEFT, RIGHT
from toga import Image

class Genderswapping(toga.App):

    async def action_open_file_filtered_dialog(self, widget):
        try:
            fname = await self.main_window.open_file_dialog(
                "Sélectionner une image", file_types=["png", "jpg"]
            )
            if fname is not None:
                self.label.text = f"File to open: {fname}"
            else:
                self.label.text = "No file selected!"
        except ValueError:
            self.label.text = "Open file dialog was canceled"

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        
        btn_style = Pack(flex=1)
        btn_open_filtered = toga.Button(
            "Sélectionner une photo/image",
            on_press=self.action_open_file_filtered_dialog,
            style=btn_style,
        )

        main_box = toga.Box(
            children=[
                btn_open_filtered,
            ],
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return Genderswapping()