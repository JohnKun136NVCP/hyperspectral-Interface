from core import np,Image,plt,sp
from core.path import getPath
import os
class RGB:
    def __init__(self,pathSelect:list,nameOutput:str): #UI selects by list. NameOutPut typed by User
        self.pathClass = getPath()
        self.pathSelect = pathSelect
        self.file_hdr, self.file_cube = self.pathClass.extentionOutput(self.pathSelect)
        self.file_output = nameOutput
        self.data_shape = None
        self.nbands = None
        self.nrows = None
        self.ncolums = None
        self.__bands = [0,0,0]
        self.min_val = 0
        self.max_val = 0
        self.ganance_r = 0 
        self.ganance_g = 0
        self.ganance_b = 0
        self.k_r = -1
        self.showGraph = False
        self.data = None
    def changeBands(self,r:int,g:int,b:int):
        self.__bands = [r,g,b]
        return self.__bands
    def __changeData(self,data):
        self.data = data
        return self.data
    def __changeValues(self,image,data)->tuple:
        self.data_shape = data.shape
        self.nbands = image.nbands
        self.nrows = image.nrows
        self.ncolums = image.ncols
        return self.data_shape,self.nbands,self.nrows,self.ncolums
    def changeMinMaxV(self,min_val,max_val) ->tuple:
        self.min_val = min_val
        self.max_val = max_val
        return self.min_val,self.max_val
    def changeGanance(self,gr:float,gg:float,gb:float) ->tuple:
        self.ganance_r = gr
        self.ganance_g = gg
        self.ganance_b = gb
        return self.ganance_r,self.ganance_g,self.ganance_b
    def changeK(self,k:int):
        if k>=-1 and k<=90:
            self.k_r = k
            return self.k_r
        else:return self.k_r
    def changeShowG(self,value:bool):
        self.showGraph = value
        return self.showGraph
    def __valuesMath(self):
        self.rgb_image -= self.min_val
        self.rgb_image /= self.max_val
        # Apply ganance of coeficients
        self.rgb_image[:, :, 0] *= self.ganance_r
        self.rgb_image[:, :, 1] *= self.ganance_g
        self.rgb_image[:, :, 2] *= self.ganance_b
        #Make sure the values are between 0,1
        self.rgb_image = np.clip(self.rgb_image, 0, 1)
        # Image (format 8 bits, 0-255)
        self.rgb_image = (self.rgb_image * 255).astype(np.uint8)
        self.rgb_image_t= np.transpose(self.rgb_image, axes=(1,0,2))
        # Rotate the image 90 degrees clockwise
        self.rgb_image_r = np.rot90(self.rgb_image_t,k=self.k_r) # k=-1 for 90 degrees clockwise
        return self.rgb_image_r
    def onclick_graph(self,event):
        if event.inaxes is not None:
            x, y = int(event.xdata), int(event.ydata)
            if 0<= x < self.data.shape[1] and 0 <= y < self.data.shape[0]:
                espectro = self.data[y, x, :]
                espectro = espectro.flatten()
                varx = range(1, espectro.shape[0] + 1)
                plt.close('all')
                fig, ax = plt.subplots() 
                ax.plot(varx, espectro) 
                ax.set_xlabel('Bands') 
                ax.set_ylabel('Reflectance')
                ax.set_title(f'Pixel spectrum ({x}, {y})') 
                plt.draw()
            else:
                print(f"Click outside the image boundaries: ({x}, {y})")

    def __showGraph(self,value:bool,rotated):
        if value:
            fig, ax = plt.subplots()
            ax.imshow(rotated)
            fig.canvas.mpl_connect('button_press_event',self.onclick_graph)
            plt.show()
            plt.close(fig)   
        
    def run(self):

        if getPath().sameLengh(self.file_hdr,self.file_cube) and len(self.file_hdr)==1:
            self.image = sp.envi.open(self.file_hdr[0],self.file_cube[0]) #Load ENVI format
            self.data = self.image.load()
            self.__changeData(self.data)
            self.__changeValues(self.image,self.data)
            self.rgb_image = self.data[:, :, self.__bands].astype(np.float32)
            self.rgb_image_r = self.__valuesMath()
            self.__showGraph(self.showGraph,self.rgb_image_r)
       
    
#How it works
"""
path = []
output = str
rgb = (pathSelect=path,nameOutput=output)
#To change bands
rgb.changeBands(int,int,int)
#Change Values (min,max)
rgb.changeMinMaxV(0,500)
#Change K- rotation [-1,90]
rgb.changeK(2)
# Change ganance 
rgb.changeGanance(float,float,float)
#Show graphs
rgb.changeShowG(bool)
#run algorithm
rgb.run()

"""