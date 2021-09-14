from django.contrib import (
    admin,
    messages,
)

from django.utils.html import (
    format_html,
)

from pictures.load import (
    ImageProcess,
    download_image_from_url,
)
from pictures.models import (
    Images,
)


class ImagesAdminView(admin.ModelAdmin):
    """
    Класс для работы с объектами модели Images в админке
    """

    def get_form(self, request, obj=None, **kwargs):
        """
        Скрывает / устанавливает только для чтения поля в зависимости от того, создаем объект или редактируем
        """
        if not obj:
            # если это новый объект, скроем поля ширины, высоты, родительского изображения
            self.exclude = ("width", 'height', 'parent_picture', 'name')
            self.readonly_fields = tuple()
        else:
            self.exclude = tuple()
            self.readonly_fields = ('picture', 'url', 'parent_picture', 'name')
        form = super(ImagesAdminView, self).get_form(request, obj, **kwargs)
        return form

    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        """
        Выводим корректное сообщение, если объект не был создан
        """
        if not getattr(self, 'sucsess', True):
            message = format_html(
                'The object has not been modified or upload.'
            )
            level = messages.ERROR
        super(ImagesAdminView, self).message_user(request=request, message=message, level=level)

    def save_model(self, request, obj, form, change):

        if change:
            if obj.picture:
                # если пользователь сразу указывает url и картинку, дополнительно ничего сохранять не надо
                if obj.height or obj.width:

                    file_name, file_extension = obj.get_file_name_and_extention()
                    new_image = ImageProcess(
                            original_image=obj,
                            extention=file_extension,
                            height=obj.height,
                            width=obj.width,
                            file_name=file_name,
                        ).create_new_obj_image()

                    if not new_image:
                        # передадим кастомный атрибут, чтобы вывести корректное сообщение
                        setattr(self, 'sucsess', False)
                    return
                setattr(self, 'sucsess', True)

        else:
            if obj.picture:
                # если пользоваетль сразу загружает файл, то сохраняем объект вместе с url, если он был указан
                setattr(self, 'sucsess', True)
                return super().save_model(request, obj, form, change)
            if obj.url:
                # если пользователь указывает только url, то предварительно загружаем изображение по url
                result = download_image_from_url(obj=obj, url=obj.url)
                if result:
                    setattr(self, 'sucsess', True)
                    return super(ImagesAdminView, self).save_model(request, obj, form, change)

                # если результата нет, устанавливаем  атрибут для вывода сообщения
                setattr(self, 'sucsess', False)


admin.site.register(Images, ImagesAdminView)
