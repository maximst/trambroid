# Generated by Django 3.2.7 on 2021-09-23 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drupal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='language',
            field=models.CharField(choices=[('ru', 'Русский'), ('en', 'English')], default='ru', max_length=5),
        ),
        migrations.AlterField(
            model_name='forum',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='forum',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='forum',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
