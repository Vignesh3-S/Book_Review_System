# Generated by Django 4.0.6 on 2023-04-28 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_alter_book_booktype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='bookfile',
            field=models.FileField(upload_to='audio/', verbose_name='Review File'),
        ),
    ]
