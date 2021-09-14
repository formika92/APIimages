# Generated by Django 2.2.10 on 2021-09-14 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('picture', models.ImageField(blank=True, max_length=255, null=True, upload_to='media')),
                ('width', models.IntegerField(blank=True, null=True, verbose_name='Ширина')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='Высота')),
                ('parent_picture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pictures.Images')),
            ],
        ),
    ]
