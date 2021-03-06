import cv2 as cv
import numpy as np
from PIL import Image, ImageFont, ImageDraw

class Converter():
    def __init__(self, resizing_scale=0.10):
        """initialised the converter class by setting the neccesary variables"""
        
        #path to the image file which you want to convert
        path = r"Images/mam.jpg"
        self.reszing_scale = resizing_scale 
        self.reading_img(path)
    
    
    def reading_img(self,path):
        """Reading the image from the given path"""

        img = cv.imread(path)
        height, width = img.shape[0],img.shape[1]
        print(f"Original image Dimenstions: height={img.shape[0]}px width={img.shape[1]}px channels={img.shape[2]}px")
        self.resizing(img,height,width)
    def resizing(self,img,height,width):
        """reszing the image so we don't get too big text file"""
        
        print("Resizing Image...")
        img = cv.resize(img,(int(width*self.reszing_scale),int(height*self.reszing_scale)),interpolation=cv.INTER_AREA)
        resized_height, resized_width = img.shape[0],img.shape[1]
        print(f"Resized image Dimenstions: height={img.shape[0]}px width={img.shape[1]}px channels={img.shape[2]}px")
        self.grayscaling(img,resized_height,resized_width)
    
    
    def grayscaling(self,img,height,width):
        """Graysclaing the image because we only need to deal with pixel intensities"""

        print("Graying the image...")
        grayed_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        self.converting_to_ascii(grayed_img,height,width)
    
    
    def converting_to_ascii(self, grayed_img,height,width):
        """Visiting each pixel of the resized gray image and converting it into
        a ASCII Character based on the pixel's intesity"""

        print("Converting to Characters...")
        ascii = ['@#','#S','S%','%?','??',"**",";;",":-","-,",",.",",,"]
        string = ""
        img_string = ""
        for i in range(height):
            for j in range(width):
                string += ascii[-(grayed_img[i][j])//25]
                img_string += ascii[-(grayed_img[i][j])//25]
            string+="\n"

        print("Finished converting...")
        self.writing_to_file(string)
        self.saving_image(img_string,height,width)
    
    
    def writing_to_file(self,string):
        """Writing the string to a text file so we can easily access it later"""

        print("Writing results to a text file")
        with open("text.txt","w") as file:
            file.write(string)
        
        print("Success!!!.. Enjoy the Masterpiece")
        
        
    def Creating_PIL_image(self,width,height,vertical_font_pixels,horizontal_font_pixels,font_size):
        """PIL stands for python image librabry. we need to create a image using PIL
        becauce in OpenCV we don't have monospaced(every letter takes same area) font.
        so we use PIL to Draw on the image using external monospaced font. after its
        done we convert the image back to OpenCV format which is numpy array"""

        new_img = np.zeros((vertical_font_pixels*height,horizontal_font_pixels*width*2,3),dtype="uint8")# mltiplying width by 2 because we are using two characters for one pixel

        #we need monospaced text inorder to achive the final output and opencv doesnt have monospaced fonts so we need to use PIL
        # Make into PIL Image
        pil_img = Image.fromarray(new_img)

        # Get a drawing context
        draw = ImageDraw.Draw(pil_img)

        #loading font
        monospace = ImageFont.truetype(r"Fonts/font.ttf",font_size)

        return pil_img,draw,monospace

    
    def saving_image(self,string,height,width):
        """This method enables to save the text output in an image """

        #Each letter of Roberto Mono(the font we are using here) of size 6 takes 4 pixels horizontally and we know it takes 8 vertically
        #so we just multiply these values with the width and height of the resized image so we have exact size of the image we need
        #remember this values will only work for Roberto Mono of size 6 for values higher than 6 you need roughly increase 1 digit of pixel values for every 2 digit increace in size value
        vertical_font_pixels = 9
        horizontal_font_pixels = 5
        font_size = 8

        pil_img,draw,monospace = self.Creating_PIL_image(width,height,vertical_font_pixels,horizontal_font_pixels,font_size)

        increment = 0
        y_increment = 0
        
        for i in range(height):
            #using PIL draw method to write Monospaced text over PIL image
            #we are using vertical_font_pixels here because its the exact number of vertical pixels our letter takes
            draw.text((2,vertical_font_pixels*(y_increment)),string[0+increment:(width*2)+increment],(255,255,255),font=monospace)
            increment+=(width*2)
            y_increment+=1
        cv.imshow("win",np.array(pil_img))
        cv.waitKey(0)

        self.saving_colored_image(width,height,string,vertical_font_pixels,horizontal_font_pixels,font_size)

        #saving the image (third argument is to get the maximum available quality for the image)
        # cv.imwrite("Output/Converted_image.jpg",np.array(pil_img),[int(cv.IMWRITE_JPEG_QUALITY),100])

    def saving_colored_image(self,width,height,string,vertical_font_pixels,horizontal_font_pixels,font_size):
        """Saves the image in Colored format"""
        ascii = {'@#':(191, 191, 175),
                 '#S':(85, 189, 255),
                 'S%':(0, 12, 140),
                 '%?':( 14, 27, 191),
                 '??':(0, 204, 249),
                 "**":(0, 204, 249),
                 ";;":(85, 189, 255),
                 ":-":(0, 204, 249),
                 "-,":( 14, 27, 191),
                 ",.":(191, 191, 175),
                 ",,":(0, 12, 140),
                 }
        
        pil_img,draw,monospace = self.Creating_PIL_image(width,height,vertical_font_pixels,horizontal_font_pixels,font_size)
        
        index = 0
        increment = 0
        p = 2
        for i in range(height):
            for j in range(width):
                color = ascii[string[0+index*p:p+index*2]]
                characters = string[0+index*p:p+index*2]
                
                draw.text((horizontal_font_pixels*2*j, vertical_font_pixels*i),characters,color,font=monospace)
                index+=1
                increment+=2

        cv.imshow("win",np.array(pil_img))
        cv.waitKey(0)

Converter()