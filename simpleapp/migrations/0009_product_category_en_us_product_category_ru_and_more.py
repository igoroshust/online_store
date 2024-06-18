# Generated by Django 5.0.3 on 2024-06-18 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpleapp', '0008_category_name_en_us_category_name_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_en_us',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='simpleapp.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_ru',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='simpleapp.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='product',
            name='description_en_us',
            field=models.CharField(max_length=200, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='product',
            name='description_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='category name', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en_us',
            field=models.CharField(help_text='category name', max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(help_text='category name', max_length=100, null=True, unique=True),
        ),
    ]