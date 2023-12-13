import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil


class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Application d'Images")

        # Création d'un gestionnaire d'onglets
        self.tabControl = ttk.Notebook(self)

        # Premier onglet
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Méthode traditionnelle')
        self.setup_tab1()

        # Deuxième onglet
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text='Méthode par apprentissage')
        self.setup_tab2()

        self.tabControl.pack(expand=1, fill="both")

    def setup_tab1(self):
        # Création d'un cadre pour l'onglet 1
        frame = ttk.Frame(self.tab1)
        frame.pack(padx=10, pady=10)

        # Création d'un bouton pour sélectionner une image
        btn_select_image = ttk.Button(frame, text="Sélectionner une image", command=self.load_image_tab1)
        btn_select_image.grid(row=0, column=0, pady=10)

        # Création d'un choix déroulant
        options_gender = ["Femme", "Homme"]
        options_male = ["Afghan", "Afro-Américain", "Allemand", "Anglais", "Argentin", "Autrichien", "Cambodgien",
                        "Chinois", "Coréen", "Ethiopien", "Français", "Grec", "Indien", "Indien (sud)", "Iranien",
                        "Iraquien", "Irlandais", "Mexicain", "Saoudien", "Taïwanais"]
        options_female = ["Africaine (centre)", "Africaine (sud)", "Africaine (ouest)", "Afro-Américaine", "Allemande",
                         "Anglaise", "Birmane", "Cambodgienne", "Coréenne", "Africaine", "Chinoise", "Grecque",
                         "Indienne", "Italienne", "Mexicaine", "Ouzbèke", "Polonaise", "Russe", "Suédoise", "Suisse",
                         "Taïwanaise"]
        self.dropdown_tab1 = ttk.Combobox(frame, values=options_male)
        self.dropdown_tab1.grid(row=2, column=0, pady=10)

        self.dropdown_tab2 = ttk.Combobox(frame, values=options_female)
        self.dropdown_tab2.grid(row=3, column=0, pady=10)

        # Image affichée
        self.image_label_tab1 = ttk.Label(frame)
        self.image_label_tab1.grid(row=1, column=0)

    def load_image_tab1(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            image = Image.open(file_path)
            image = image.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            self.image_label_tab1.config(image=photo)
            self.image_label_tab1.image = photo

    def setup_tab2(self):
        # Création d'un cadre pour l'onglet 2
        frame = ttk.Frame(self.tab2)
        frame.pack(padx=10, pady=10)

        # Création d'un bouton pour sélectionner une image
        btn_select_image = ttk.Button(frame, text="Sélectionner une image", command=self.load_image_tab2)
        btn_select_image.grid(row=0, column=0, pady=10)

        # Bouton sous l'image
        btn_tab2 = ttk.Button(frame, text="Bouton Onglet 2", command=self.button_click_tab2)
        btn_tab2.grid(row=1, column=0, pady=10)

        # Image affichée
        self.image_label_tab2 = ttk.Label(frame)
        self.image_label_tab2.grid(row=2, column=0)

    def load_image_tab2(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            image = Image.open(file_path)
            image = image.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            self.image_label_tab2.config(image=photo)
            self.image_label_tab2.image = photo

    def button_click_tab2(self):
        print("Bouton Onglet 2 cliqué")


if __name__ == "__main__":
    app = ImageApp()
    app.geometry("800x600")
    app.mainloop()
