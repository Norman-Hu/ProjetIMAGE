import tkinter as ttk
from tkinter import filedialog
import customtkinter
from PIL import Image, ImageTk

# Listage des options
options_gender = ["", "Femme", "Homme"]
options_default = [""]
options_male = ["", "Afghan", "Afro-Américain", "Allemand", "Anglais", "Argentin", "Autrichien", "Cambodgien",
                "Chinois", "Coréen", "Ethiopien", "Français", "Grec", "Indien", "Indien (sud)", "Iranien",
                "Iraquien", "Irlandais", "Mexicain", "Saoudien", "Taïwanais"]
options_female = ["", "Africaine (centre)", "Africaine (sud)", "Africaine (ouest)", "Afro-Américaine", "Allemande",
                  "Anglaise", "Birmane", "Cambodgienne", "Coréenne", "Africaine", "Chinoise", "Grecque",
                  "Indienne", "Italienne", "Mexicaine", "Ouzbèke", "Polonaise", "Russe", "Suédoise", "Suisse",
                  "Taïwanaise"]

def open_input_dialog_event():
    dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
    print("CTkInputDialog:", dialog.get_input())


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.title("Application Genderswap")
        self.geometry(f"{1100}x{580}")

        # Création du tabview
        self.tabview = customtkinter.CTkTabview(self, width=1060)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Méthode traditionnelle")
        self.tabview.add("Méthode par apprentissage")
        self.tabview.tab("Méthode traditionnelle").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Méthode par apprentissage").grid_columnconfigure(0, weight=1)

        # -- Tab méthode traditionnelle --

        # Image sélectionnée
        self.image_label_tab1 = ttk.Label(self.tabview.tab("Méthode traditionnelle"))
        self.image_label_tab1.grid(row=0, column=0)

        # Bouton de sélection d'image
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Méthode traditionnelle"),
                                                           text="Sélectionner une image",
                                                           command=self.load_image)
        self.string_input_button.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Choix du genre
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Méthode traditionnelle"), dynamic_resizing=False,
                                                        values=options_gender, command=self.gender_callback)
        self.optionmenu_1.grid(row=2, column=0, padx=20, pady=(10, 10))

        # Choix de l'ethnie
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Méthode traditionnelle"),
                                                    values=options_default)
        self.combobox_1.grid(row=3, column=0, padx=20, pady=(10, 10))

        # -- Tab méthode par apprentissage --
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Méthode par apprentissage"), text="Blblblbl to do but flemme atm")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")])

        if file_path:
            image = Image.open(file_path)
            image = image.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            self.image_label_tab1.config(image=photo)
            self.image_label_tab1.image = photo

    def gender_callback(self, choice):
        if choice == "":
            self.combobox_1.configure(values=options_default)
            self.combobox_1.set("")
        if choice == "Femme":
            self.combobox_1.configure(values=options_female)
            self.combobox_1.set("")
        if choice == "Homme":
            self.combobox_1.configure(values=options_male)
            self.combobox_1.set("")


if __name__ == "__main__":
    app = App()
    app.mainloop()