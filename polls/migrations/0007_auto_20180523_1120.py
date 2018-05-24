# Generated by Django 2.0.4 on 2018-05-23 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20180523_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='image_url',
            field=models.ImageField(default='', upload_to='polls'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
