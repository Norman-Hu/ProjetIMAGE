import tkinter as ttk
from tkinter import filedialog
import customtkinter
from CTkMessagebox import CTkMessagebox
import os
from PIL import Image, ImageTk
import utilities
import shutil

# Listage des options
options_gender = ["", "Femme", "Homme"]
options_default = [""]
options_male = ["", "Afghan", "Afro-Américain", "Allemand", "Anglais", "Argentin", "Autrichien", "Cambodgien",
                "Chinois", "Coréen", "Ethiopien", "Français", "Grec", "Indien", "Indien (sud)", "Iranien",
                "Iraquien", "Irlandais", "Mexicain", "Saoudien", "Taïwanais"]
options_female = ["", "Africaine (centre)", "Africaine (sud)", "Africaine (ouest)", "Afro-Américaine", "Allemande",
                  "Anglaise", "Birmane", "Cambodgienne", "Coréenne", "Chinoise", "Grecque",
                  "Indienne", "Indienne (sud)", "Italienne", "Mexicaine", "Ouzbèke", "Polonaise", "Russe", "Suédoise",
                  "Suisse", "Taïwanaise"]


def resize_photo(image):
    width, height = image.size
    if width > height:
        new_height = 300 * height / width
        image = image.resize((300, int(new_height)), Image.LANCZOS)
    else:
        new_width = 300 * width / height
        image = image.resize((int(new_width), 300), Image.LANCZOS)
    return image


def open_input_dialog_event():
    dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
    print("CTkInputDialog:", dialog.get_input())


class App(customtkinter.CTk):
    width = 1100
    height = 650

    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.title("Application Genderswap")
        self.geometry(f"{1100}x{650}")

        # Création du fond
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "./gradient.png"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        #
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="ns")

        # Création du tabview
        self.tabview = customtkinter.CTkTabview(self.main_frame, width=500)
        self.tabview.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Méthode traditionnelle")
        self.tabview.add("Méthode par apprentissage")
        self.tabview.tab("Méthode traditionnelle").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Méthode par apprentissage").grid_columnconfigure(0, weight=1)

        # -- Tab méthode traditionnelle --

        # Affichage de l'image sélectionnée (initialisée par défaut)
        self.image_path_1 = ""
        self.image_label_tab1 = ttk.Label(self.tabview.tab("Méthode traditionnelle"))
        self.image_label_tab1.grid(row=0, column=0)
        default_image = Image.open("./default.png")
        default_photo = ImageTk.PhotoImage(default_image)
        self.image_label_tab1.config(image=default_photo)
        self.image_label_tab1.image = default_photo
        self.image_tosave_1 = Image.open("./default.png")
        self.res_path_1 = ""

        # Bouton de sélection d'image
        self.upload_button_1 = customtkinter.CTkButton(self.tabview.tab("Méthode traditionnelle"),
                                                           text="Sélectionner une image",
                                                           command=self.load_image_1)
        self.upload_button_1.grid(row=1, column=0, padx=20, pady=(10, 5))

        # Bouton de téléchargement d'image
        self.download_button_1 = customtkinter.CTkButton(self.tabview.tab("Méthode traditionnelle"),
                                                     text="Télécharger une image",
                                                     command=self.save_image_1)
        #self.download_button_1.grid(row=2, column=0, padx=20, pady =(5, 10))

        # Choix du genre
        self.label_gender = customtkinter.CTkLabel(self.tabview.tab("Méthode traditionnelle"),
                                                  text="Genre désiré")
        self.label_gender.grid(row=3, column=0, padx=20)
        self.combobox_gender_1 = customtkinter.CTkComboBox(self.tabview.tab("Méthode traditionnelle"),
                                                        values=options_gender, command=self.gender_callback)
        self.combobox_gender_1.grid(row=4, column=0, padx=20)

        # Choix de l'ethnie
        self.label_ethnicity = customtkinter.CTkLabel(self.tabview.tab("Méthode traditionnelle"),
                                                  text="Ethnie désirée")
        self.label_ethnicity.grid(row=5, column=0, padx=20)
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Méthode traditionnelle"),
                                                    values=options_default)
        self.combobox_1.grid(row=6, column=0, padx=20)

        # Bouton de validation
        self.start_button = customtkinter.CTkButton(self.tabview.tab("Méthode traditionnelle"),
                                                     text="Genderswapper",
                                                     command=self.genderswap_trad)
        self.start_button.grid(row=7, column=0, padx=20, pady=(20, 10))

        # -- Tab méthode par apprentissage --

        # Affichage de l'image sélectionnée (initialisée par défaut)
        self.image_path_2 = ""
        self.image_label_tab2 = ttk.Label(self.tabview.tab("Méthode par apprentissage"))
        self.image_label_tab2.grid(row=0, column=0)
        default_image = Image.open("./default.png")
        default_photo = ImageTk.PhotoImage(default_image)
        self.image_label_tab2.config(image=default_photo)
        self.image_label_tab2.image = default_photo
        self.image_tosave_2 = Image.open("./default.png")
        self.res_path_2 = ""

        # Bouton de sélection d'image
        self.upload_button_2 = customtkinter.CTkButton(self.tabview.tab("Méthode par apprentissage"),
                                                     text="Sélectionner une image",
                                                     command=self.load_image_2)
        self.upload_button_2.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Bouton de téléchargement d'image
        self.download_button_2 = customtkinter.CTkButton(self.tabview.tab("Méthode traditionnelle"),
                                                         text="Télécharger une image",
                                                         command=self.save_image_2)
        #self.download_button_2.grid(row=2, column=0, padx=20, pady=(5, 10))

        # Choix du genre
        self.label_gender = customtkinter.CTkLabel(self.tabview.tab("Méthode par apprentissage"),
                                                   text="Genre désiré")
        self.label_gender.grid(row=2, column=0, padx=20)
        self.combobox_gender_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Méthode par apprentissage"),
                                                        dynamic_resizing=False,
                                                        values=options_gender, command=self.gender_callback)
        self.combobox_gender_2.grid(row=3, column=0, padx=20)

        # Bouton de validation
        self.start_button = customtkinter.CTkButton(self.tabview.tab("Méthode par apprentissage"),
                                                    text="Genderswapper",
                                                    command=self.genderswap_appr)
        self.start_button.grid(row=6, column=0, padx=20, pady=(20, 10))

    def load_image_1(self): # Demande à l'utilisateur de sélectionner une image locale
        self.image_path_1 = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")])

        if self.image_path_1:
            image = Image.open(self.image_path_1)
            image = resize_photo(image)
            photo = ImageTk.PhotoImage(image)

            self.image_label_tab1.config(image=photo)
            self.image_label_tab1.image = photo
            self.image_tosave_1 = Image.open(self.image_path_1)

    def load_image_2(self): # Demande à l'utilisateur de sélectionner une image locale
        self.image_path_2 = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")])

        if self.image_path_2:
            image = Image.open(self.image_path_2)
            image = resize_photo(image)
            photo = ImageTk.PhotoImage(image)

            self.image_label_tab2.config(image=photo)
            self.image_label_tab2.image = photo

    def save_image_1(self):
        print(self.res_path_1)
        if self.res_path_1 != "":
            selected_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                          filetypes=[("Fichiers image", "*.png;*.jpg;*.jpeg")])
            if selected_path:
                shutil.copyfile(self.res_path_1, selected_path)

    def save_image_2(self):
        if self.res_path_2 != "":
            selected_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("Fichiers image", "*.png;*.jpg;*.jpeg")])
            if selected_path:
                shutil.copyfile(self.res_path_2, selected_path)

    def gender_callback(self, choice): # Met à jour le choix de l'ethnie en fonction du genre choisi
        if choice == "":
            self.combobox_1.configure(values=options_default)
            self.combobox_1.set("")
        if choice == "Femme":
            self.combobox_1.configure(values=options_female)
            self.combobox_1.set("")
        if choice == "Homme":
            self.combobox_1.configure(values=options_male)
            self.combobox_1.set("")

    def genderswap_trad(self):
        file_path = self.image_path_1
        if file_path == "":
            CTkMessagebox(title="Erreur", message="Veuillez sélectionner une image !", icon="cancel")
            return
        gender = self.combobox_gender_1.get()
        if gender == "":
            CTkMessagebox(title="Erreur", message="Veuillez sélectionner le genre désiré !", icon="cancel")
            return
        ethnicity = self.combobox_1.get()
        if ethnicity == "":
            CTkMessagebox(title="Erreur", message="Veuillez sélectionner l'ethnie désirée !", icon="cancel")
            return
        target_path = "./target_images/"
        if gender == "Femme" :
            target_path = target_path + "Women_population/" + utilities.corresp_ethnicity_female[ethnicity]
        else :
            target_path = target_path + "Men_population/" + utilities.corresp_ethnicity_male[ethnicity]
        result_path = "./result_trad_temp.jpg"
        utilities.traditional_method(file_path, target_path, result_path)

        image = Image.open(result_path)
        image = resize_photo(image)
        photo = ImageTk.PhotoImage(image)
        self.image_label_tab1.config(image=photo)
        self.image_label_tab1.image = photo
        self.image_tosave_1 = Image.open(result_path)
        self.res_path_1 = result_path

    def genderswap_appr(self):
        file_path = self.image_path_2
        if file_path == "":
            CTkMessagebox(title="Erreur", message="Veuillez sélectionner une image !", icon="cancel")
            return
        gender = self.combobox_gender_2.get()
        if gender == "":
            CTkMessagebox(title="Erreur", message="Veuillez sélectionner le genre désiré !", icon="cancel")
            return
        if gender == "Femme":
            new_path = "./CycleGAN/test/testA/img.png"
        else:
            new_path = "./CycleGAN/test/testB/img.png"

        res_loc = "./results/experiment_name/test_latest/images/img_fake.png"
        shutil.copyfile(file_path, new_path)
        utilities.cyclegan_method(gender)

        image = Image.open(res_loc)
        image = resize_photo(image)
        photo = ImageTk.PhotoImage(image)
        self.image_label_tab2.config(image=photo)
        self.image_label_tab2.image = photo
        self.image_tosave_2 = Image.open(res_loc)
        self.res_path_2 = res_loc


if __name__ == "__main__":
    app = App()
    app.mainloop()
