# Import modules
from core import (np,
                  Image, 
                  plt, 
                  sp, 
                  envi,
                  principal_components, 
                  imshow,
                  defaultdict,
                  mpimg)
from core.path import getPath

class PCA:
    def __init__(self):
        self.hdr = str
        self.cube = str
        self.float = str
        self.img = None
        self.principalC = list()
        self.data = list()
        self.img_array = list()
        self.ordered_files = []

    def pca(self, l_images: list, path: str) -> tuple[list, list]:
        """
        Processes a list two elements at a time, saving each pair into two variables.
        """
        for i in range(0, len(l_images), 2):
            if i + 1 < len(l_images):  # Ensure there's a second item
                cube_file = l_images[i]
                hdr_file = l_images[i + 1]
                img = envi.open(path + hdr_file, path + cube_file)
                data = img.asarray()
                data = data.astype(np.float32)
                pc = principal_components(img)
                self.principalC.append(pc.cov)
                pc_0999 = pc.reduce(fraction=0.999)
                img_pc = pc_0999.transform(img)
                self.img_array.append(img_pc)
        return self.principalC, self.img_array

    def showarea(self, images, cols=3):
        """
        Displays images in subplots with axes, labels, and individual titles.
        """
        num_images = len(images)
        rows = (num_images + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
        axes = axes.flatten()

        for i in range(num_images):
            img = images[i]
            ax = axes[i]
            ax.imshow(img)
            ax.set_title(f"Image {i+1}", fontsize=12)
            ax.set_xlabel("Bands", fontsize=10)
            ax.set_ylabel("Bands", fontsize=10)
            ax.tick_params(axis='both', which='both', length=6)

        # Hide unused subplots
        for j in range(num_images, len(axes)):
            axes[j].axis('off')

        plt.tight_layout()
        fig.savefig("Subplots.jpg")
        plt.show()
        plt.close()


    def normalize_image(self, img):
        """
        Normalizes image data to range [0, 1] for display.
        """
        self.img = img.astype(np.float32)
        self.img -= self.img.min()
        if self.img.max() != 0:
            self.img /= self.img.max()
        return self.img

    def showpictbands(self, images, bands:tuple, cols=3, iteration=False, number=0):
        """
        Displays selected bands of images in subplots with axes, labels, and individual titles.
        """
        num_images = len(images)
        rows = (num_images + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
        axes = axes.flatten()
        for i in range(num_images):
            img = images[i][:, :, bands]
            img = self.normalize_image(img)
            ax = axes[i]
            ax.imshow(img)
            ax.set_title(f"Image {i+1} with bands {bands}", fontsize=12)
            ax.set_xlabel("px", fontsize=10)
            ax.set_ylabel("px", fontsize=10)
            ax.tick_params(axis='both', which='both', length=6)

        for j in range(num_images, len(axes)):
            axes[j].axis('off')
        try:
            if not iteration:
                plt.tight_layout()
                fig.savefig("Subplots_2.jpg")
                plt.close()
            else:
                plt.tight_layout()
                fig.savefig(f"Subplots_{number}_bands_{bands}.jpg")
                plt.close()
        except Exception:
            number = -1
            print("Error to process information")

"""
How to use?
Example
import os
pca = PCA()
gp = getPath()
#If there are many images to analyze
files_list = gp.list_and_order_files_by_mixed_extensions(directory_path=os.getcwd(), extensions=["hdr", "cube"])
#Apply pca method to root path images
a,c = pca.pca(files_list,getPath.root())
#Export images ( pca data, bands=(a,b,c), interation (for many pictures))
pca.showpictbands(c,bands=(6,1,3),iteration=False)

"""