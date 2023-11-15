import torch
from dataset import MaleFemaleDataset
import sys
from utils import save_checkpoint, load_checkpoint
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
import config
from tqdm import tqdm
from torchvision.utils import save_image
from discriminator_model import Discriminator
from generator_model import Generator


def train_fn(disc_F, disc_M, gen_M, gen_F, loader, opt_disc, opt_gen, l1, mse, d_scaler, g_scaler):
    loop = tqdm(loader, leave=True)

    for idx, (male, female) in enumerate(loop):
        male = male.to(config.DEVICE)
        female = female.to(config.DEVICE)

        with torch.cuda.amp.autocast():
            fake_female = gen_F(male)
            D_F_real = disc_F(female)
            D_F_fake = disc_M(fake_female.detach())
            D_F_real_loss = mse(D_F_real, torch.ones_like(D_F_real))
            D_F_fake_loss = mse(D_F_fake, torch.ones_like(D_F_fake))
            D_F_loss = D_F_real_loss + D_F_fake_loss

            fake_male = gen_M(female)
            D_M_real = disc_M(male)
            D_M_fake = disc_M(fake_male.detach())
            D_M_real_loss = mse(D_M_real, torch.ones_like(D_M_real))
            D_M_fake_loss = mse(D_M_fake, torch.ones_like(D_M_fake))
            D_M_loss = D_M_real_loss + D_M_fake_loss

            D_loss = (D_F_loss + D_M_loss)/2

        opt_disc.zero_grad()
        d_scaler.scale(D_loss).backward()
        d_scaler.step(opt_disc)
        d_scaler.update()

        # Entrainement generateurs F et M
        with torch.cuda.amp.autocast():
            # adversarial loss pour les deux generateurs
            D_F_fake = disc_F(fake_female)
            D_M_fake = disc_M(fake_male)
            loss_G_F = mse(D_F_fake, torch.ones_like(D_F_fake))
            loss_G_M = mse(D_M_fake, torch.ones_like(D_M_fake))

            # cycle loss
            cycle_male = gen_M(fake_female)
            cycle_female = gen_F(fake_male)
            cycle_male_loss = l1(male, cycle_male)
            cycle_female_loss = l1(female, cycle_female)

            # identity loss
            identity_male = gen_M(male)
            identity_female = gen_F(female)
            identity_male_loss = l1(male, identity_male)
            identity_female_loss = l1(female, identity_female)

            # addition de tous
            G_loss = (
                loss_G_M
                + loss_G_F
                + cycle_male_loss * config.LAMBDA_CYCLE
                + cycle_female_loss * config.LAMBDA_CYCLE
                + identity_female_loss * config.LAMBDA_IDENTITY
                + identity_male_loss * config.LAMBDA_IDENTITY
            )

        opt_gen.zero_grad()
        g_scaler.scale(G_loss).backward()
        g_scaler.step(opt_gen)
        g_scaler.update()

        if idx % 200 == 0:
            save_image(fake_female*0.5+0.5, f"saved_images/female_{idx}.png")
            save_image(fake_male*0.5+0.5, f"saved_images/male_{idx}.png")


def main():
    disc_F = Discriminator(in_channels=3).to(config.DEVICE)
    disc_M = Discriminator(in_channels=3).to(config.DEVICE)
    gen_M = Generator(img_channels=3, num_residuals=9).to(config.DEVICE)
    gen_F = Generator(img_channels=3, num_residuals=9).to(config.DEVICE)
    opt_disc = optim.Adam(
        list(disc_F.parameters()) + list(disc_M.parameters()),
        lr=config.LEARNING_RATE,
        betas=(0.5, 0.999)
    )
    opt_gen = optim.Adam(
        list(gen_M.parameters()) + list(gen_F.parameters()),
        lr=config.LEARNING_RATE,
        betas=(0.5, 0.999)
    )

    L1 = nn.L1Loss()
    mse = nn.MSELoss()

    if config.LOAD_MODEL:
        load_checkpoint(
            config.CHECKPOINT_GEN_F, gen_F, opt_gen, config.LEARNING_RATE
        )
        load_checkpoint(
            config.CHECKPOINT_GEN_M, gen_M, opt_gen, config.LEARNING_RATE
        )
        load_checkpoint(
            config.CHECKPOINT_CRITIC_F, disc_F, opt_disc, config.LEARNING_RATE
        )
        load_checkpoint(
            config.CHECKPOINT_CRITIC_M, disc_M, opt_disc, config.LEARNING_RATE
        )

    dataset = MaleFemaleDataset(
        root_male=config.TRAIN_DIR+"/male", root_female=config.TRAIN_DIR+"/female", transform=config.transforms
    )
    loader = DataLoader(
        dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        num_workers=config.NUM_WORKERS,
        pin_memory=True
    )
    g_scaler = torch.cuda.amp.GradScaler()
    d_scaler = torch.cuda.amp.GradScaler()

    for epoch in range(config.NUM_EPOCHS):
        train_fn(disc_F, disc_M, gen_M, gen_F, loader, opt_disc, opt_gen, L1, mse, d_scaler, g_scaler)

        if config.SAVE_MODEL:
            save_checkpoint(gen_F, opt_gen, filename=config.CHECKPOINT_GEN_F)
            save_checkpoint(gen_M, opt_gen, filename=config.CHECKPOINT_GEN_M)
            save_checkpoint(disc_F, opt_disc, filename=config.CHECKPOINT_CRITIC_F)
            save_checkpoint(disc_M, opt_disc, filename=config.CHECKPOINT_CRITIC_M)


if __name__ == "__main__":
    main()
