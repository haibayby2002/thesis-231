import customtkinter
import os
import cv2 as cv
from PIL import Image
from tkinter import filedialog as fd
from polyroi import Shape


class AppConfig(object):
    __slots__ = ()
    # app_dir = os.path.dirname(os.path.realpath(__file__)
    title = "Traffic Congestion GUI"
    geometry = "700x450"
    author = "Nguyen Quy Hai"
    organization = "BKU HCMUT"
    logo = "bku_logo.jpg"  # CustomTkinter_logo_single.png
    icon = {"video": "video-file-icon-28.png"}
    video_type = [("video", "avi"), ("video", "mp4")]


conf = AppConfig()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.import_file = ""
        self.export_file = ""
        self.mqtt_url = ""

        self.cap = ""

        # self.title("image_example.py")
        self.title(conf.title)
        self.geometry(conf.geometry)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # region load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.initial_path = os.path.dirname(os.path.realpath(__file__))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, conf.logo)), size=(26, 26))
        self.image_preview = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                                    size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                                 size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.video_icon = customtkinter.CTkImage(Image.open((os.path.join(image_path, conf.icon["video"]))))
        # endregion

        # region create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  " + conf.organization,
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.export_csv_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                         border_spacing=10, text="Export CSV",
                                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                                         hover_color=("gray70", "gray30"),
                                                         image=self.chat_image, anchor="w",
                                                         command=self.export_csv_button_event)
        self.export_csv_button.grid(row=2, column=0, sticky="ew")

        self.pub_mqtt_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                       border_spacing=10, text="Publish MQTT",
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       hover_color=("gray70", "gray30"),
                                                       image=self.add_user_image, anchor="w",
                                                       command=self.pub_mqtt_button_event)
        self.pub_mqtt_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        # endregion

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_image_preview = customtkinter.CTkLabel(self.home_frame, text="", image=self.image_preview)
        self.home_frame_image_preview.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_open = customtkinter.CTkButton(self.home_frame, text="", image=self.video_icon,
                                                              command=self.button_video_open_event)
        self.home_frame_button_open.grid(row=1, column=0, padx=20, pady=10)

        self.home_frame_poly_checkbox = customtkinter.CTkCheckBox(self.home_frame, text="Cut Polygon")
        self.home_frame_poly_checkbox.grid(row=2, column=0, padx=20, pady=10)

        self.home_frame_file_label = customtkinter.CTkLabel(self.home_frame, text=self.import_file, compound="right")
        self.home_frame_file_label.grid(row=3, column=0, padx=20, pady=10)

        # create second frame
        self.export_excel = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.export_csv_button.configure(fg_color=("gray75", "gray25") if name == "export_csv" else "transparent")
        self.pub_mqtt_button.configure(fg_color=("gray75", "gray25") if name == "pub_mqtt" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "export_csv":
            self.export_excel.grid(row=0, column=1, sticky="nsew")
        else:
            self.export_excel.grid_forget()
        if name == "pub_mqtt":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    # region Nav
    def home_button_event(self):
        self.select_frame_by_name("home")

    def export_csv_button_event(self):
        self.select_frame_by_name("export_csv")

    def pub_mqtt_button_event(self):
        self.select_frame_by_name("pub_mqtt")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # endregion

    def button_video_open_event(self):
        try:
            temp = fd.askopenfile(
                initialdir=self.initial_path + '/test_videos',
                filetypes=conf.video_type
            )
            self.import_file = temp.name
            self.home_frame_file_label.configure(text=self.import_file)
        except:
            pass
        finally:
            if self.import_file != "":
                self.select_roi()

        print(self.import_file)

    def select_roi(self):
        self.cap = cv.VideoCapture(self.import_file)
        _, img = self.cap.read()

        if self.home_frame_poly_checkbox.get():  # Polygon
            shape = Shape.get_roi(img)
            for point in shape.points:
                print(point.x, point.y)
                # Todo: numpy, calculate area, mass with image

        else:  # Rectangle
            roi = cv.selectROI(img)
            img = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
            cv.imshow("Demo", img)
            self.image_preview = Image.fromarray(img.astype('uint8')[...,::-1], "RGB")
            self.image_preview.show("Pillow")
            # self.home_frame_image_preview.configure(image=self.image_preview)

    def visualization(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
