import glob
import os
import shutil

import face_recognition
import numpy as np
from PIL import Image, ImageDraw


def info(message):
    print(f'[INFO] {message}')


def get_all_files(folder):
    info(f'Getting all files from *{folder}*')
    cur_direc = os.getcwd()
    path = os.path.join(cur_direc, f'{folder}/')
    return [f for f in glob.glob(path + '*.jpg')]


# def check_face(file):
#     info('Check if image have a face')
#     image = face_recognition.load_image_file(file)
#     face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
#
#     if len(face_locations) > 0:
#         info('Face founded!')
#         cur_direc = os.getcwd()
#         path = os.path.join(cur_direc, 'founded_unknown_faces/')
#         name = file.replace(cur_direc, "").replace('\\test\\', '')
#         target_path = f"{path}/{name}"
#
#         shutil.copy(file, target_path)
#         info('Saved in unknown_faces')
#         if os.path.isfile(file):
#             os.remove(file)
#         info('Removed old file')


def check_file(file, faces_encodings, faces_names):
    info(f'Start checking file: {file}')
    unknown_image = face_recognition.load_image_file(file)

    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)
    cur_direc = os.getcwd()

    if len(face_locations) == 0:
        info('Face not founded!')
        path = os.path.join(cur_direc, 'no_faces/')
        name = file.replace(cur_direc, "").replace('\\test\\', '')
        target_path = f"{path}/{name}"
        shutil.move(file, target_path)
        info('Saved in *no_faces*')
        if os.path.isfile(file):
            os.remove(file)
        info('Removed old file')

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        if os.path.isfile(file):
            matches = face_recognition.compare_faces(faces_encodings, face_encoding)

            face_distances = face_recognition.face_distance(faces_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                info('Have a match')
                name = faces_names[best_match_index]
                draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
                text_width, text_height = draw.textsize(name)
                draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255),
                               outline=(0, 0, 255))
                draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
                # pil_image.show()

                path = os.path.join(cur_direc, 'checked/')
                target_path = f"{path}/{name}.jpg"
                count = 0
                while os.path.isfile(target_path):
                    target_path = f"{path}/{name}_{count}.jpg"
                    count += 1
                shutil.copy(file, target_path)
                info('Saved')
                if os.path.isfile(file):
                    os.remove(file)
                info('Removed old file')
            else:
                info('Unknown face founded!')
                path = os.path.join(cur_direc, 'founded_unknown_faces/')
                name = file.replace(cur_direc, "").replace('\\test\\', '')
                target_path = f"{path}/{name}"
                shutil.copy(file, target_path)
                info('Saved in *unknown_faces*')
                if os.path.isfile(file):
                    os.remove(file)
                info('Removed old file')
    del draw


def my_identity():
    info('Init...')
    faces_encodings = []
    faces_names = []
    cur_direc = os.getcwd()
    list_of_files = get_all_files('faces')
    number_files = len(list_of_files)
    names = list_of_files.copy()
    for i in range(number_files):
        globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
        globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
        faces_encodings.append(globals()['image_encoding_{}'.format(i)])
        names[i] = names[i].replace(cur_direc, "").replace('\\faces\\', '').replace('.jpg', '')
        faces_names.append(names[i])

    total_files = len(get_all_files("test"))
    info(f'Total files: {total_files}')
    for i, file in enumerate(get_all_files('test')):
        info(f'Checkin {i} in {total_files}')
        check_file(file, faces_encodings, faces_names)
        print('=' * 100)


if __name__ == '__main__':
    my_identity()
