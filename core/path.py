import os

class getPath:
    def __init__(self):
       self.root = str #Main root path 
       self.cube_path = [] #Cube name 
       self.hdr_path = [] # HDR name
       self.output_name = str # Output name
       #Const elements
       self.__hdr_ext = ".hdr"
       self.__cube_ext = ".cube"

    def extentionOutput(self, pathFiles: list) -> tuple[list, list]:
        hdr_path, cube_path = [], []
        for path in pathFiles:
            if not isinstance(path, str):
                continue
            full_path = os.path.abspath(path)   # <--- aquí
            _, extension = os.path.splitext(path)
            if extension == self.__hdr_ext:
                hdr_path.append(full_path)
            elif extension == self.__cube_ext:
                cube_path.append(full_path)
        return (hdr_path, cube_path)


    def sameLengh(self,a:list,b:list) -> bool:
        if len(a) == len(b):return True