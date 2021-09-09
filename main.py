import glob
import os
import shutil
import time

import face_recognition
import numpy as np
from PIL import Image, ImageDraw

faces_encodings = []
faces_names = []


def info(message):
    print(f'[INFO] {message}')


def get_all_files(folder):
    info(f'Getting all files from *{folder}*')
    cur_direc = os.getcwd()
    path = os.path.join(cur_direc, f'{folder}/')
    return [f for f in glob.glob(path + '*.jpg')]


def copy_file_to_folder(file, dist_dir, name=None, remove=True):
    cur_direc = os.getcwd()
    path = os.path.join(cur_direc, f'{dist_dir}/')
    if not os.path.isdir(path):
        os.mkdir(path)
    if name is None:
        name = file.replace(cur_direc, '').replace('\\test\\', '').replace('.jpg', '')
    target_path = f'{path}/{name}.jpg'
    count = 0
    while os.path.isfile(target_path):
        target_path = f'{path}/{name}_{count}.jpg'
        count += 1
    shutil.copy(file, target_path)
    info(f'Saved in {dist_dir}')
    if os.path.isfile(file) and remove:
        os.remove(file)
        info('Removed old file')


def check_file(file):
    global faces_names, faces_encodings
    info(f'Start checking file: {file}')
    unknown_image = face_recognition.load_image_file(file)

    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    if len(face_locations) == 0:
        info('Face not founded!')
        copy_file_to_folder(file, 'no_faces')

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(faces_encodings, face_encoding)
        face_distances = face_recognition.face_distance(faces_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            info('Have a match')
            name = faces_names[best_match_index]
            copy_file_to_folder(file, 'checked', name=name, remove=False)
        else:
            info('Unknown face founded!')
            pil_image = Image.fromarray(unknown_image)
            draw = ImageDraw.Draw(pil_image)
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
            time.sleep(1)
            pil_image.show()
            answer = input('Did you know this face? Y/n (Y is default): ')
            if answer == 'Y' or answer == 'y' or answer is None or answer == '':
                name = input('Write the name: ')
                copy_file_to_folder(file, 'faces', name=name, remove=False)
                init()
            if answer == 'N' or answer == 'n':
                copy_file_to_folder(file, 'founded_unknown_faces', remove=False)

    if os.path.isfile(file):
        os.remove(file)
        info('Removed old file')


def init():
    info('Init...')
    global faces_names, faces_encodings
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


def my_identity():
    init()
    all_files = get_all_files("test")
    total_files = len(all_files)
    info(f'Total files: {total_files}')
    for i, file in enumerate(all_files):
        info(f'Checkin {i} in {total_files}. {total_files - i} files await.')
        check_file(file)
        print('=' * 100)
    info('PROGRESS DONE')


if __name__ == '__main__':
    # k_k()
    my_identity()
