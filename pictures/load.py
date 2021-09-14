import io
import os
import sys
import urllib
from io import (
    BytesIO,
)

from PIL import (
    Image,
)
from django.core.files import File
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
)

from picture_project.enum import FormatsImagesEnum
from pictures.models import (
    Images,
)


class ImageProcess:
    """
    Меняет высоту и ширину файла
    """

    def __init__(
            self,
            original_image,
            extention: str,
            height,
            width,
            file_name=None
    ):
        self.__original_image = original_image
        self.__height = height
        self.__width = width
        self.__extention = extention if extention != FormatsImagesEnum.jpg else FormatsImagesEnum.jpeg
        self.__file_name = file_name
        self.new_img_name = None

    def __resize_image(self):
        """
        Меняет размер изображения до его сохранения
        """
        tmp_file = io.BytesIO(self.__original_image.read())
        image = Image.open(tmp_file).resize((self.__width, self.__height), Image.ANTIALIAS)
        new_image = io.BytesIO()
        image.save(new_image, 'PNG')
        return new_image

    def get_image(self):
        """
        Возвращает измененное изображение
        """
        return self.__resize_image()

    def change_load_image(self):
        """
        Меняет высоту и ширину ранее сохраненного файла
        """
        with Image.open(self.__original_image.picture) as image:
            img = None
            bytes_obj = None

            picture_height = self.__original_image.picture.height
            picture_width = self.__original_image.picture.width

            user_height = self.__height
            user_width = self.__width

            # проверяем, совпадает ли размер изображения с указанным пользователем, если нет, меняем его
            if (
                    (user_height != picture_height)
                    or (user_width != picture_width)
            ):
                # пользователь может менять только ширину или высоту,
                # тогда при отсутствии новых данных будем брать ширину/высоту оригинальной картинки
                self.__height = picture_height if not user_height else user_height
                self.__width = picture_width if not user_width else user_width

                img = image.resize((int(self.__width), int(self.__height)))

                bytes_obj = BytesIO()
                img.save(bytes_obj, format=self.__extention)

        return img, bytes_obj

    def new_image_name(self):
        """
        Создает новое имя файла, содержащее высоту и ширину
        """
        self.new_img_name = f'{self.__file_name}.{self.__extention.lower()}'  # для передачи в функцию

    def get_uploaded_image(self):
        image_file = None

        image, bytes_obj = self.change_load_image()

        if image and bytes_obj:
            image_file = InMemoryUploadedFile(
                bytes_obj,
                'ImageField',
                self.new_img_name,
                f'image/{self.__extention}',
                sys.getsizeof(bytes_obj),
                None,
            )

        return image_file

    def create_new_obj_image(self):
        """
        Создает и сохраняет новый объект изображения
        """
        new_image = None
        uploaded_image = self.get_uploaded_image()
        if isinstance(uploaded_image, InMemoryUploadedFile):
            self.new_image_name()

            new_image = Images()
            new_image.height = self.__height
            new_image.width = self.__width
            new_image.picture.save(self.new_img_name, uploaded_image)
            new_image.parent_picture = self.__original_image
            new_image.save()

        return new_image


def download_image_from_url(obj, url):
    """
    Скачивает картинку по url и сохраняет её в ImageField объекта
    """
    try:
        result = urllib.request.urlretrieve(url)
    except ValueError:
        result = None
    else:
        obj.picture.save(
            os.path.basename(url),
            File(open(result[0], 'rb'))
        )

    return result
