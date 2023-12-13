import os
import cv2
import numpy as np
import subprocess
import face_utils
import ImageProcessing

corresp_ethnicity_male = {
    "Afghan": "Afghanistan.png",
    "Afro-Américain": "African_american.png",
    "Allemand": "German.png",
    "Anglais": "England.png",
    "Argentin": "Argentina.png",
    "Autrichien": "Austria.png",
    "Cambodgien": "Cambodia.png",
    "Chinois": "China.png",
    "Coréen": "Korea.png",
    "Ethiopien": "Ethiopia.png",
    "Français": "France.png",
    "Grec": "Greece.png",
    "Indien": "India.png",
    "Indien (sud)": "South_india.png",
    "Iranien": "Iran.png",
    "Iraquien": "Iraq.png",
    "Irlandais": "Ireland.png",
    "Mexicain": "Mexico.png",
    "Saoudien": "Saudi_arabia.png",
    "Taïwanais": "Taiwan.png"
}

corresp_ethnicity_female = {
    "Africaine (centre)": "Central_African.png",
    "Africaine (sud)": "South_Africa.png",
    "Africaine (ouest)": "West_african.png",
    "Afro-Américaine": "African_American.png",
    "Allemande": "German.png",
    "Anglaise": "English.png",
    "Birmane": "Burmese.png",
    "Cambodgienne": "Cambodian.png",
    "Coréenne": "Korean.png",
    "Chinoise": "Chinese.png",
    "Grecque": "Greek.png",
    "Indienne": "Indian.png",
    "Indienne (sud)": "South_indian.png",
    "Italienne": "Italian.png",
    "Mexicaine": "Mexican.png",
    "Ouzbèke": "Uzbek.png",
    "Polonaise": "Polish.png",
    "Russe": "Russian.png",
    "Suédoise": "Swedish.png",
    "Suisse": "Swiss.png",
    "Taïwanaise": "Taiwanese.png"
}


def traditional_method(dest_img_path, target_img_path, result_path='result.jpg'):
    dest_img = cv2.imread(dest_img_path)
    target_img = cv2.imread(target_img_path)

    dest_xyz_landmark_points, dest_landmark_points = face_utils.get_face_landmark(dest_img)
    dest_convexhull = cv2.convexHull(np.array(dest_landmark_points))

    target_img_hist_match = ImageProcessing.hist_match(target_img, dest_img)

    _, target_landmark_points = face_utils.get_face_landmark(target_img)
    target_convexhull = cv2.convexHull(np.array(target_landmark_points))

    new_face, result = face_utils.face_swapping(dest_img, dest_landmark_points, dest_xyz_landmark_points,
                                                dest_convexhull, target_img, target_landmark_points, target_convexhull,
                                                return_face=True)

    height, width, _ = dest_img.shape
    h, w, _ = target_img.shape
    rate = width / w
    cv2.imwrite(result_path, result)
    cv2.waitKey(0)


def cyclegan_method(gender):
    if gender == "Homme":
        direction = 'BtoA'
    else:
        direction = 'AtoB'
    script_path = "./CycleGAN/test.py"
    subprocess.run(["python3", script_path, "--dataroot", "CycleGAN/test", "--direction", direction, "--dataset_mode", "single", "--model", "test", "--no_dropout" ])

    """
    if gender == "Homme":
        cycle_gan.config.direction = 'BtoA'
    else:
        cycle_gan.config.direction = 'AtoB'
    opt = TestOptions().parse()
    opt.num_threads = 0
    opt.batch_size = 1
    opt.serial_batches = True
    opt.no_flip = True
    opt.display_id = -1
    dataset = cycle_gan.data.create_dataset(opt)
    model = create_model(opt)
    model.setup(opt)

    web_dir = os.path.join(opt.results_dir, opt.name,
                           '{}_{}'.format(opt.phase, opt.epoch))  # define the website directory
    webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.epoch))

    for i, data in enumerate(dataset):
        if i >= opt.num_test:  # only apply our model to opt.num_test images.
            break
        model.set_input(data)  # unpack data from data loader
        model.test()
        visuals = model.get_current_visuals()  # get image results
        img_path = model.get_image_paths()  # get image paths
        save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize,
                    use_wandb=opt.use_wandb)
    webpage.save()  # save the HTML
    """

# Ensemble des fonctions et méthodes nécessaires à l'utilisation du cyclegan entraîné


def create_model(opt):
    instance = TestModel(opt)
    return instance
"""
def create_dataset(opt):
    data_loader = CustomDatasetDataLoader(opt)
    dataset = data_loader.load_data()
    return dataset





class CustomDatasetDataLoader:
    def __init__(self, opt):
        self.opt = opt
        self.dataset = SingleDataset(opt)
        self.dataloader = torch.utils.data.DataLoader(
            self.dataset,
            batch_size=opt.batch_size,
            shuffle=not opt.serial_batches,
            num_workers=int(opt.num_threads))

    def load_data(self):
        return self

    def __len__(self):
        return min(len(self.dataset), self.opt.max_dataset_size)

    def __iter__(self):
        for i, data in enumerate(self.dataloader):
            if i * self.opt.batch_size >= self.opt.max_dataset_size:
                break
            yield data
"""