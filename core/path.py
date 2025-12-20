import os
from core.libs import defaultdict,envi,imshow
class getPath:
    def __init__(self):
       self.root = str #Main root path 
       self.cube_path = [] #Cube name 
       self.hdr_path = [] # HDR name
       self.output_name = str # Output name
       self.ordered_files = [] # Mixed files
       #Const elements
       self.__hdr_ext = ".hdr"
       self.__cube_ext = ".cube"
    @staticmethod
    def root() -> str:
        return os.getcwd()+'/'
    def extentionOutput(self, pathFiles: list) -> tuple[list, list]:
        hdr_path, cube_path = [], []
        for path in pathFiles:
            if not isinstance(path, str):
                continue
            full_path = os.path.abspath(path)
            _, extension = os.path.splitext(path)
            if extension == self.__hdr_ext:
                hdr_path.append(full_path)
            elif extension == self.__cube_ext:
                cube_path.append(full_path)
        return (hdr_path, cube_path)
    
    def list_and_order_files_by_mixed_extensions(self, directory_path:str, extensions:list):
        """
        Lists and orders files by shared prefix across multiple extensions,
        but only includes groups with mixed extensions. Groups with only one extension are ignored.
        """
        extensions = set(ext.lower() for ext in extensions)
        prefix_groups = defaultdict(list)
        unmatched_files = []

        for filename in os.listdir(directory_path):
            full_path = os.path.join(directory_path, filename)
            if os.path.isfile(full_path):
                name, ext = os.path.splitext(filename)
                ext = ext[1:].lower()
                if ext in extensions:
                    prefix = name.split('-')[0]
                    prefix_groups[prefix].append((filename, ext))

        for prefix in sorted(prefix_groups.keys()):
            group = prefix_groups[prefix]
            unique_exts = set(ext for _, ext in group)
            if len(unique_exts) > 1:
                self.ordered_files.extend(filename for filename, _ in sorted(group))
            else:
                unmatched_files.extend(filename for filename, _ in group)

        self.ordered_files.extend(sorted(unmatched_files))
        return self.ordered_files
    def saveImgs(self, path, imgarray, nameSave=None, auto=False):
        """
        Saves a list of image arrays with ENVI headers.
        """
        save_path = os.path.join(path, "Saved")
        os.makedirs(save_path, exist_ok=True)

        for idx, img in enumerate(imgarray):
            description = input(f"Enter a description of figure {idx+1}: ")
            header_info = {
                'description': description,
                'bands': str(img.shape[2]),
                'lines': str(img.shape[0]),
                'samples': str(img.shape[1]),
                'interleave': 'bip',
                'data type': '4'
            }

            try:
                if auto:
                    filename = f"{nameSave or 'image'}_{idx+1}.hdr"
                else:
                    filename = input(f"Enter filename for image {idx+1} (with .hdr extension): ")

                output_image = os.path.join(save_path, filename)
                envi.save_image(output_image, img, metadata=header_info, interleave='bip', force=True)
                print(f"Image saved to {output_image} and {output_image.replace('.hdr', '.img')}")

            except Exception as e:
                print(f"Error saving image {idx+1}: {e}")
    def pcaShow(self):
        if os.path.exists(self.path):
            if all(map(str, self.__dataPaths())):
                _, _ = self.__pcaMethod(self.data[0], self.data[1])
                v = imshow(self.img_pc[:, :, self.bands], stretch_all=True)
        else:
            print("Error!")


    def sameLengh(self,a:list,b:list) -> bool:
        if len(a) == len(b):return True