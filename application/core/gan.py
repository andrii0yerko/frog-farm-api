import torch
from torch import nn
from PIL import Image
from torchvision.transforms import ToPILImage  #TODO: rewrite tensor->image transformation without torchvision
import io

class Generator(nn.Module):

    def __init__(self, z_dim=100, im_chan=3, hidden_dim=64):
        super(Generator, self).__init__()
        self.z_dim = z_dim
        self.gen = nn.Sequential(
            nn.ConvTranspose2d( z_dim, hidden_dim * 8, kernel_size=4,
                               stride=1, padding=0, bias=False),
            nn.BatchNorm2d(hidden_dim * 8),
            nn.ReLU(True),
            nn.ConvTranspose2d(hidden_dim * 8, hidden_dim * 4, kernel_size=4,
                               stride=2, padding=1, bias=False),
            nn.BatchNorm2d(hidden_dim * 4),
            nn.ReLU(True),
            nn.ConvTranspose2d(hidden_dim * 4, hidden_dim * 2, kernel_size=4,
                               stride=2, padding=1, bias=False),
            nn.BatchNorm2d(hidden_dim * 2),
            nn.ReLU(True),
            nn.ConvTranspose2d(hidden_dim * 2, hidden_dim, kernel_size=4,
                               stride=2, padding=1, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU(True),
            nn.ConvTranspose2d(hidden_dim, im_chan, kernel_size=4,
                               stride=2, padding=1, bias=False),
            nn.Tanh()
        )

    def unsqueeze_noise(self, noise):
        return noise.view(len(noise), self.z_dim, 1, 1)

    def forward(self, noise):
        x = self.unsqueeze_noise(noise)
        return self.gen(x)


class GANGenerator():
    PATH = './frog-gan-v1.pt'
    z_dim = 100
    hidden_dim = 64
    
    def __init__(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = Generator(z_dim=self.z_dim, hidden_dim=self.hidden_dim).to(self.device)
        self.model.load_state_dict(torch.load(self.PATH, map_location=self.device))
        self.model.eval()

    def generate_image(self):
        noise = self.get_noise()
        image_tensor = self.model(noise)
        image_tensor = (image_tensor.cpu() + 1) / 2
        image = ToPILImage()(image_tensor[0])
        image = image.resize((128, 128), resample=0)
        with io.BytesIO() as f:
            image.save(f, format='JPEG')
            img_byte_arr = f.getvalue()
        return img_byte_arr
    
    def get_noise(self, n_samples=1):
        return torch.randn(n_samples, self.z_dim, device=self.device)