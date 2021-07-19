# image cartoonizer using opencv2
# importing the required modules
import cv2 #image processing 
import easygui #open the filebox
import numpy as np  #store image and process them as numbers 
import imageio #read an image from a particular path 
import sys 
import matplotlib.pyplot as plot #visualize data 
import os 
import tkinter as tk #library to make GUIs 
from tkinter import *


top=tk.Tk()
photo = PhotoImage(file = "Circle-icons-image.png")
top.iconphoto(False, photo)
top.geometry('900x600')
top.title('Image Cartoonizer')
top.configure(background='gray')
label=Label(top,background='#808080', font=('Arial',20,'bold'))


#opens a box to choose a file :) 
def upload():
    path=easygui.fileopenbox()
    cartoonize(path)

#makes all changes to get to the cartoonized image at the end 
#of transformation 
def cartoonize(Path):
    #reading the image 
    ogi=cv2.imread(Path)
    ogi=cv2.cvtColor(ogi,cv2.COLOR_BGR2RGB)

    #validate the image 
    if ogi is None:
        print("Error File is Not An Image Try Again :) !")
        sys.exit()
    
    RS1=cv2.resize(ogi,(960,540))

    #convert colored image to grayscale
    grayScaleImage= cv2.cvtColor(ogi,cv2.COLOR_BGR2GRAY)
    RS2= cv2.resize(grayScaleImage,(960,540))

    #median blur to smoothen the image 
    smooth=cv2.medianBlur(grayScaleImage,5)
    RS3=cv2.resize(smooth,(960,540))

    #retrieve the edges usin thresholding thechnique 
    edge=cv2.adaptiveThreshold(smooth,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 9, 9)
    RS4= cv2.resize(edge,(960,540))

    #bilateral filtering to remove noise 
    cim=cv2.bilateralFilter(ogi,9,300,300)
    RS5=cv2.resize(cim,(960,540))

    #making edge image 
    cartoon=cv2.bitwise_and(cim,cim,mask=edge)
    RS6=cv2.resize(cartoon,(960,540))
    #list of all images we transformed above 
    listOfImgs =[RS1,RS2,RS3,RS4,RS5,RS6]

    fig,axes=plot.subplots(3,2, figsize=(8,8),subplot_kw={'xticks':[], 'yticks':[]},gridspec_kw=dict(hspace=0.1,wspace=0.1))
    
    for i,ax in enumerate(axes.flat):
        ax.imshow(listOfImgs[i], cmap='gray')

    store=Button(top,text="Save Cartoonized Image",command=lambda:save(RS6,Path),padx=30,pady=5)
    store.configure(background='#a2c0ff',foreground="black",font=('calibri',14,'bold'))
    store.pack(side=TOP,pady=50)

    plot.show()

def save(RS6,pathh):
    #saving an image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname(pathh)
    extension=os.path.splitext(pathh)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(RS6, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

upload=Button(top,text="Cartoonize Your Image",command=upload,padx=10,pady=5)
upload.configure(background='#a2c0ff', foreground='black',font=('lucida',14,'bold'))
upload.pack(side=TOP,pady=50)


top.mainloop()
    


