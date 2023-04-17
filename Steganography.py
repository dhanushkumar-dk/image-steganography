from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from PIL import ImageTk
from PIL import Image
from tkinter import messagebox
from io import BytesIO
import  os

class Stegno:
    output_image_size = 0
    def main(self,root):
        root.title('ImageSteganography')
        root.geometry('500x600')
        root.configure(bg = 'POWDERBLUE')
        root.resizable(width = False, height = False)
        frame1 = Frame(root, bg = 'POWDERBLUE')
        lbl_tit = Label(frame1, text = 'IMAGE STEGAOGRAPHY', fg = 'BLUE', bg = 'POWDERBLUE', font = ('radioland', 33, 'bold'))
        btn_enc = Button(frame1, text = "Encode", font=('courier', 20, 'bold'), fg = 'WHITE', bg = 'RED'  , padx=14, command = lambda :self.frame1_encode(frame1))
        btn_dec = Button(frame1, text = "Decode", font=('courier', 20, 'bold'), fg = 'WHITE', bg = 'GREEN', padx=14, command = lambda :self.frame1_decode(frame1))
        root.grid_rowconfigure(   1, weight = 1)
        root.grid_columnconfigure(0, weight = 1)
        frame1.grid()
        lbl_tit.grid(row = 1, pady = 50)
        btn_enc.grid(row = 2, pady = 40)
        btn_dec.grid(row = 3, pady = 12)
        
    def frame1_encode(self, f):
        f.destroy()
        frame1_enc = Frame(root, bg='POWDERBLUE')
        lbl_OutP = Label( frame1_enc, font = ('courier', 70, 'bold'), bg = 'POWDERBLUE', fg = 'BLACK', text = 'OUTPUT')
        lbl_info = Label( frame1_enc, font = ('courier', 18, 'bold'), bg = 'POWDERBLUE', fg = 'BLUE' , text = 'Select Image to hide information')
        btn_slct = Button(frame1_enc, font = ('courier', 18), bg = 'GREEN', fg = 'BLUE' , text = 'Select', command = lambda : self.frame2_encode(frame1_enc ))
        btn_back = Button(frame1_enc, font = ('courier', 18), bg = 'RED'  , fg = 'BLUE' , text = 'Cancel', command = lambda : Stegno.home(self, frame1_enc  ))
        lbl_OutP.grid(row = 1, pady = 50)
        lbl_info.grid()
        btn_slct.grid(pady = 15)
        btn_back.grid()
        frame1_enc.grid()
        
    def frame2_encode(self,f2):
        ep = Frame(root, bg = 'POWDERBLUE')
        myfile = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error","You have selected nothing !")
        else:
            myimg   = Image.open(myfile)
            myimage = myimg.resize((300, 200))
            img     = ImageTk.PhotoImage(myimage)
            lbl_slct = Label(ep, text = 'Selected Image', font=('courier', 18, 'bold'), bg = 'POWDERBLUE', fg = 'BLUE')
            lbl_slct.grid()
            panel       = Label(ep, image = img)
            panel.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = myimg.size
            panel.grid()
            l2 = Label(ep, text = 'Enter the message', font = ('courier', 18, 'bold'), bg = 'POWDERBLUE', fg = 'BLUE')
            l2.grid(pady = 15)
            text_area = Text(ep, width = 50, height = 10)
            text_area.grid()
            data = text_area.get("1.0", "end-1c")
            btn_encode = Button(ep, text = 'Encode', font = ('courier', 11), bg = 'GREEN', command = lambda : [self.enc_fun(text_area, myimg), Stegno.home(self, ep)])          # BACK
            btn_cancel = Button(ep, text = 'Cancel', font = ('courier', 11), bg = 'RED', command = lambda :  Stegno.home(self, ep)) 
            btn_encode.grid(pady = 15)
            btn_cancel.grid()
            ep.grid(row = 1)
            f2.destroy()
            
    def enc_fun(self, text_area, myimg):
        # Storing parameter values to Variable data
        data = text_area.get("1.0", "end-1c")

        # If the Message is not given show Message Box
        if (len(data) == 0):
            messagebox.showinfo("Alert","Kindly enter text in TextBox")
        else:
            newimg = myimg.copy()
            self.encode_enc(newimg, data)
            my_file = BytesIO()
            temp    = os.path.splitext(os.path.basename(myimg.filename))[0]
            newimg.save(tkinter.filedialog.asksaveasfilename(initialfile = temp, filetypes = ([('png', '*.png')]), defaultextension = ".png"))
            self.d_image_size = my_file.tell()
            self.d_image_w, self.d_image_h = newimg.size
            messagebox.showinfo("Success","Encoding Successful\nFile is saved as Image_with_hiddentext.png in the same directory")
            
    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)
        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1
                
    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        for i in range(lendata):
            # Extracting 3 pixels at a time
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]
            # Pixel value should be made
            # odd for 1 and even for 0
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                    if (pix[j] % 2 != 0):
                        pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
            # Eigh^th pixel of every set tells
            # whether to stop or read further.
            # 0 means keep reading; 1 means the
            # message is over.
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1
            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def genData(self, data):
        newd = []
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd
    
    def frame1_decode(self, frame1):
        frame1.destroy()        
        d_f2 = Frame(root, bg = 'POWDERBLUE')
        label_art   = Label( d_f2, text = 'OUTPUT'                        , font = ('courier', 70 , 'bold'), bg = 'POWDERBLUE')
        l1          = Label( d_f2, text = 'Select Image with Hidden text', font = ('courier', 18, 'bold'), bg = 'POWDERBLUE', fg = 'blue')
        bws_button  = Button(d_f2, text = 'Select', font = ('courier', 18), bg = 'GREEN', command = lambda : self.frame2_decode(d_f2))
        back_button = Button(d_f2, text = 'Cancel', font = ('courier', 18), bg = 'RED'  , command = lambda : Stegno.home(self, d_f2)) 
        label_art.grid(row = 1, pady = 50)
        l1.grid()
        bws_button.grid()
        back_button.grid(pady = 15)
        back_button.grid()
        d_f2.grid()

    def frame2_decode(self, d_f2):
        d_f3 = Frame(root, bg = 'POWDERBLUE')
        myfile = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error","You have selected nothing !")
        else:
            myimg = Image.open(myfile, 'r')
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l4 = Label(d_f3,text = 'SELECTED IMAGE', fg = 'blue', bg = 'POWDERBLUE', font = ('courier', 18, 'bold'))
            l4.grid()
            panel = Label(d_f3, image = img)
            panel.image = img
            panel.grid()
            hidden_data = self.decode(myimg)
            l2 = Label(d_f3, text='HIDDEN DATA', fg = 'green', bg = 'POWDERBLUE', font=('courier', 18, 'bold'))
            l2.grid(pady=10)
            text_area = Text(d_f3, width = 50, height = 10)
            text_area.insert(INSERT, hidden_data)
            text_area.configure(state = 'disabled')
            text_area.grid()
            back_button = Button(d_f3, text = 'Cancel', bg = 'RED', font = ('courier', 12, 'bold'), command = lambda :self.page3(d_f3))
            back_button.grid(pady = 15)
            back_button.grid()
            show_info = Button(d_f3, text = 'More Info', bg = 'ORANGE', font = ('courier', 12, 'bold'), command = self.info)
            show_info.grid()
            d_f3.grid(row = 1)
            d_f2.destroy()

    def decode(self, image):
        data = ''
        imgdata = iter(image.getdata())

        while (True):
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data
            
    def info(self):
        try:
            str = 'original image:-\nsize of original image:{}mb\nwidth: {}\nheight: {}\n\n' \
                  'decoded image:-\nsize of decoded image: {}mb\nwidth: {}' \
                '\nheight: {}'.format(self.output_image_size.st_size/1000000,
                                    self.o_image_w,self.o_image_h,
                                    self.d_image_size/1000000,
                                    self.d_image_w,self.d_image_h)
            messagebox.showinfo('info',str)
        except:
            messagebox.showinfo('Info','Unable to get the information')
            
    def page3(self, frame):
        frame.destroy()
        self.main(root)
        
    def home(self, frame):
            frame.destroy()
            self.main(root)
            
root = Tk()
obj = Stegno()
obj.main(root)
root.mainloop()
