

class FormatsImagesEnum:
    """
    Список поддерживаемых форматов
    """
    jpeg = 'JPEG'
    jpg = 'JPG'
    png = 'PNG'
    formats_images_tuple = (png, jpeg, jpg)


class MessageEnum:
    """
    Список сообщений
    """
    msg_not_exist = 'Запрашиваемое изображение не существует'
    msg_not_resize = 'Не переданы параметры ширины и/или высоты для изменения'
    msg_uncorrect_format = 'Неверный формат изображения'
