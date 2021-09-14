import os

from django.db import (
    models,
)
from django.db.models.signals import (
    pre_delete,
)
from django.dispatch import (
    receiver,
)


class Images(models.Model):
    """
    Модель для хранения картинок
    """
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    picture = models.ImageField(
        upload_to='media',
        null=True,
        max_length=255,
        blank=True,
    )

    width = models.IntegerField(
        verbose_name='Ширина',
        null=True,
        blank=True,
    )
    height = models.IntegerField(
        verbose_name='Высота',
        null=True,
        blank=True,
    )

    parent_picture = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # будем очищать поле при удалении
    )

    class Meta:
        verbose_name_plural = "Images"

    def __str__(self):
        return f'{self.name}_{self.width}x{self.height}'

    def get_file_name_and_extention(self):
        """
        Достает из объекта Image название файла и расширение
        """
        original_name = self.picture.name
        file_name, file_extension = os.path.splitext(original_name)

        if '/' in file_name:
            file_name = file_name.partition('/')[-1]
        file_extension = file_extension.partition('.')[-1].upper()

        return file_name, file_extension

    def save(self, *args, **kwargs):

        result = True
        if self.url and not self.picture:
            # если пользователь указал url, но не загрузил картинку, или ранее её не загружали в объект, то
            # грузим картинку из url
            from pictures.load import download_image_from_url
            result = download_image_from_url(obj=self, url=self.url)
        # при добавлении нового объекта будем сохранять значения ширины и высоты из значений картинки
        if kwargs.get('need_change_size', True):
            if self.picture:
                self.width = self.picture.width
                self.height = self.picture.height

        # если пользователь не указывает имя, будем сохранять имя из названия файла
        if not self.name:
            new_name = self.picture.name
            if new_name:
                if '/' in new_name:
                    new_name = new_name.partition('/')[-1]
                self.name = new_name
        if result:
            super().save()


@receiver(pre_delete, sender=Images)
def delete_image(sender, instance, **kwargs):
    """
    Удаляет изображение при удалении объекта
    """
    if instance.picture:
        instance.picture.delete(False)
