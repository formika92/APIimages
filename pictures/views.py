from rest_framework import (
    status,
    viewsets,
)
from rest_framework.parsers import (
    MultiPartParser,
    FileUploadParser,
)
from rest_framework.response import (
    Response,
)

from rest_framework.decorators import (
    action,
)

from picture_project.enum import (
    FormatsImagesEnum, MessageEnum,
)
from .load import ImageProcess
from .models import (
    Images,
)
from .serialaizers import (
    ImageListSerialaizer,
    ImageSerializer,
)


class ImageList(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageListSerialaizer
    parser_classes = (MultiPartParser, FileUploadParser,)

    def get(self, request, **kwargs):
        """
        Отображает информацию об изображениях
        """
        all_images = Images.objects.all()
        serializer = ImageListSerialaizer(all_images, many=True)

        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        """
        Добавляет изображение
        """
        file_serializer = ImageSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True)
    def resize(self, request, pk, **kwargs):
        """
        Изменяет размер изображения
        """
        # проверяем, передавались ли в body
        height = self.request.POST.get('height')
        width = self.request.POST.get('width')

        # по необходимости можно искать в params
        # if not height or width:
        #     height = self.request.query_params.get('height') if not height else height
        #     width = self.request.query_params.get('width') if not width else width

        if height or width:
            try:
                original_image = Images.objects.get(pk=pk)
            except Images.DoesNotExist:
                return Response(
                    {'result': MessageEnum.msg_not_exist}
                )

            # получаем название оригинального файла и расширение
            file_name, file_extension = original_image.get_file_name_and_extention()
            if file_extension in FormatsImagesEnum.formats_images_tuple:

                # создадим и сохраним новый объект изображения
                new_image = ImageProcess(
                    original_image=original_image,
                    extention=file_extension,
                    height=height,
                    width=width,
                    file_name=file_name
                ).create_new_obj_image()

                file_serializer = ImageSerializer(new_image)

                return Response(file_serializer.data, status=status.HTTP_201_CREATED)

            return Response({'result': MessageEnum.msg_uncorrect_format})

        else:
            return Response({'result': MessageEnum.msg_not_resize})
