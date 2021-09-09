import os
import time

import face_recognition
from PIL import Image as PImage, ImageDraw
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput


class MainApp(App):
    def __init__(self):
        super().__init__()
        self.cur_dir = os.getcwd()
        self.reject_button = Button(text="I don't know", font_size=14)
        self.accept_button = Button(text="This one", font_size=14)
        self.detect_face = Button(text="Detect face", font_size=14)
        self.name_input = TextInput(hint_text='Put the name', multiline=False, size_hint=(1, .5),
                                    pos_hint={'center_x': .5, 'center_y': .5}, halign='center')
        self.image = Image(source=f'{self.cur_dir}\\tost\\1.jpg')

        def find_face(instance):
            print('The button <%s> is being pressed' % instance.text)
            unknown_image = face_recognition.load_image_file(f'{self.cur_dir}\\tost\\1.jpg')
            face_locations = face_recognition.face_locations(unknown_image)
            face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                pil_image = PImage.fromarray(unknown_image)
                draw = ImageDraw.Draw(pil_image)
                draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255), width=5)
                pil_image.save(f'{self.cur_dir}\\tost\\1.jpg')
            # self.image.reload()

        self.detect_face.bind(on_press=find_face)

    def build(self):
        main_box = BoxLayout(orientation='vertical', size=(300, 300))

        image_box = BoxLayout(orientation='vertical', size_hint=(1, .8))
        image_box.add_widget(self.image)

        bottom_box = BoxLayout(orientation='horizontal', size_hint=(1, .2))
        bottom_box.add_widget(self.reject_button)
        bottom_box.add_widget(self.name_input)
        bottom_box.add_widget(self.accept_button)
        bottom_box.add_widget(self.detect_face)

        main_box.add_widget(image_box)
        main_box.add_widget(bottom_box)

        return main_box


if __name__ == '__main__':
    MainApp().run()
