import customtkinter
import os
import sys
import glob
from PIL import Image

DEV = False
INITIALDIR = '~' # '~' homedir, '.' currentdir
START, END = '0.0', 'end'

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self, dev):
        super().__init__()

        self.DEV = dev
        self.icofile = 'icon.ico'
        self.title("DecreaseOnly") #downsizer, resizer
        self.resizable(False, False)
        self.geometry('+100+100')
        self.font = customtkinter.CTkFont(family='Verdana', size=14)

        # =========== frames

        self.frame_0 = customtkinter.CTkFrame(master=self, corner_radius=3)
        self.frame_0.grid(row=0, column=0, padx=10, pady=10, sticky="nwes")

        self.frame_1 = customtkinter.CTkFrame(master=self, corner_radius=3)
        self.frame_1.grid(row=1, column=0, padx=10, pady=10, sticky="nwes")

        self.frame_2 = customtkinter.CTkFrame(master=self, corner_radius=3)
        self.frame_2.grid(row=2, column=0, padx=10, pady=10, sticky="nwes")

        self.frame_9 = customtkinter.CTkFrame(master=self, corner_radius=3)
        self.frame_9.grid(row=9, column=0, padx=10, pady=10, sticky="nwes")

        # =========== frame_0

        self.text_dir = customtkinter.CTkTextbox(master=self.frame_0,
                                                 width=400,
                                                 height=0) # wrap='none'
        self.text_dir.grid(row=0, column=0, rowspan=2, pady=5, padx=10, sticky="nsw")

        self.select_btn = customtkinter.CTkButton(master=self.frame_0, 
                                                  text='Select dir', 
                                                  command=self.getdir)
        self.select_btn.grid(row=0, column=1, pady=5, padx=10, sticky="we")

        self.switch_recursive = customtkinter.CTkSwitch(master=self.frame_0,
                                                text="Recursive")
        self.switch_recursive.grid(row=1, column=1, pady=5, padx=10, sticky="")

        # =========== frame_1

        self.check_box_0 = customtkinter.CTkCheckBox(master=self.frame_1,
                                                     text=".jpg",
                                                     width=80)
        self.check_box_0.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_1,
                                                     text=".jpeg",
                                                     width=80)
        self.check_box_1.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_1,
                                                     text=".bmp",
                                                     width=80)
        self.check_box_2.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        self.check_box_3 = customtkinter.CTkCheckBox(master=self.frame_1,
                                                     text=".tiff",
                                                     width=80)
        self.check_box_3.grid(row=0, column=3, pady=10, padx=10, sticky="w")

        self.check_box_4 = customtkinter.CTkCheckBox(master=self.frame_1,
                                                     text=".png",
                                                     width=80)
        self.check_box_4.grid(row=0, column=4, pady=10, padx=10, sticky="w")

        self.check_box_list = [self.check_box_0, 
                               self.check_box_1, 
                               self.check_box_2, 
                               self.check_box_3,
                               self.check_box_4]
        
        # =========== frame_2

        self.radio_var = customtkinter.IntVar(value=1920) #default

        self.radio_2560 = customtkinter.CTkRadioButton(master=self.frame_2,
                                                        variable=self.radio_var,
                                                        value=2560,
                                                        text='2560',
                                                        width=80)
        self.radio_2560.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.radio_1920 = customtkinter.CTkRadioButton(master=self.frame_2,
                                                        variable=self.radio_var,
                                                        value=1920,
                                                        text='1920',
                                                        width=80)
        self.radio_1920.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        self.radio_1600 = customtkinter.CTkRadioButton(master=self.frame_2,
                                                        variable=self.radio_var,
                                                        value=1600,
                                                        text='1600',
                                                        width=80)
        self.radio_1600.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        self.radio_1440 = customtkinter.CTkRadioButton(master=self.frame_2,
                                                        variable=self.radio_var,
                                                        value=1440,
                                                        text='1440',
                                                        width=80)
        self.radio_1440.grid(row=0, column=3, pady=10, padx=10, sticky="w")

        self.radio_1280 = customtkinter.CTkRadioButton(master=self.frame_2,
                                                        variable=self.radio_var,
                                                        value=1280,
                                                        text='1280',
                                                        width=80)
        self.radio_1280.grid(row=0, column=4, pady=10, padx=10, sticky="w")

        self.radio_1024 = customtkinter.CTkRadioButton(master=self.frame_2,
                                                        variable=self.radio_var,
                                                        value=1024,
                                                        text='1024',
                                                        width=80)
        self.radio_1024.grid(row=0, column=5, pady=10, padx=10, sticky="w")

        # =========== frame_9

        self.text_log = customtkinter.CTkTextbox(master=self.frame_9,
                                                 width=400,
                                                 height=80) # wrap='none'
        self.text_log.grid(row=0, column=0, pady=5, padx=10, sticky="nswe")

        self.switch_overwrite = customtkinter.CTkSwitch(master=self.frame_9,
                                                text="Overwrite files",
                                                progress_color='red',
                                                button_hover_color='red')
        self.switch_overwrite.grid(row=0, column=1, pady=5, padx=10, sticky="")

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_9,
                                                        width=400)
        self.progressbar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.go_btn = customtkinter.CTkButton(master=self.frame_9, 
                                            text='Go', 
                                            command=self.go)
        self.go_btn.grid(row=1, column=1, pady=5, padx=10, sticky="we")

        # =========== default

        self.get_ico()
        self.check_box_0.select()
        self.check_box_1.select()
        self.progressbar.set(0)

    def get_ico(self):
        try:
            if self.DEV:
                self.iconbitmap(default=self.icofile)
                return
            
            path = os.path.join(sys._MEIPASS, self.icofile)
            self.iconbitmap(default=path)
        except:
            pass

    def getdir(self):
        "opens dialog to select dir. '~' homedir, '.' current dir"
        res = customtkinter.filedialog.askdirectory(initialdir=INITIALDIR)
        self.text_dir.delete(START, END)
        self.text_dir.insert(START, res)

    def go(self):
        "takes dir path from 'self.text_dir', create 'self.image_list' and run main"
        self._dir = self.text_dir.get(START, END)[:-1] # 'D:/code/project_imgpress/test_img'
        if not os.path.exists(self._dir):
            self._print('dir not exists')
            return
        
        self.get_image_list()
        if self.image_list:
            self.main()
        
    def get_image_list(self):
        "creates 'image_list' from 'self._dir' with selected extensions"
        recursive = True if self.switch_recursive.get() else False
        ext_list = tuple([i.cget('text') for i in self.check_box_list if i.get()]) # ('.jpg', '.bmp')
        ilist = glob.iglob(self._dir + '/**', recursive=recursive)  # creates files list with mask ** recursive
        self.image_list = [i.replace('\\', '/') for i in ilist if i.endswith(ext_list)]

    def main(self):
        "takes settings from GUI and decrease images"
        progress = 0
        progress_delta = 1 / len(self.image_list)
        self.text_log.delete(START, END)
        radio_select = self.radio_var.get()     # 1920
        overwrite = self.switch_overwrite.get()

        if not overwrite: # create new dir and files
            new_dir = self._dir + '_' + str(radio_select)
            self.create_dir(new_dir)

        for path in self.image_list:
            image = Image.open(path)
            size = image.size

            if not overwrite: # create new dir and files
                path = path.replace(self._dir, new_dir, 1) # make new path
                self.create_dir(os.path.dirname(path)) # create subdir

            if max(size) > radio_select:
                ratio = max(size) / radio_select
                image = image.resize((round(size[0] / ratio), round(size[1] / ratio)))
            try:
                image.save(path)
            except OSError:
                self._print(f"[Error]: {path}")

            progress += progress_delta
            self.progressbar.set(progress)
            app.update()

    def create_dir(self, dir):
        "create dir if not exists and allowed"
        if not os.path.exists(dir):
            try:
                os.mkdir(dir)
            except OSError:
                self._print(f"Cant create dir: {dir}")

    def _print(self, string: str):
        "print text to self.text_log"
        self.text_log.insert(END, string + '\n')


app = App(DEV)
app.mainloop()

