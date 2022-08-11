# Generated by Django 3.2.7 on 2021-09-23 12:09

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import parler.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20151029_1447'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'base_manager_name': '_plain_manager'},
        ),
        migrations.AlterModelOptions(
            name='blogtranslation',
            options={'default_permissions': (), 'managed': True},
        ),
        migrations.AlterModelManagers(
            name='blog',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('_plain_manager', django.db.models.manager.Manager()),
            ],
        ),
        #migrations.AddField(
            #model_name='blog',
            #name='_parler_query',
            #field=parler.fields.SingleTranslationObject('content.Blog', 'content.blogtranslation'),
        #),
        migrations.AlterField(
            model_name='blog',
            name='drupal_slug',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='blog',
            name='drupal_type',
            field=models.CharField(blank=True, default='blog', max_length=10),
        ),
        migrations.AlterField(
            model_name='blog',
            name='ip',
            field=models.GenericIPAddressField(default='127.0.0.1'),
        ),
        migrations.AlterField(
            model_name='blogtranslation',
            name='body',
            field=models.TextField(default=''),
        ),
        #migrations.AlterField(
            #model_name='blogtranslation',
            #name='master',
            #field=parler.fields.MasterKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='content.blog'),
        #),
        migrations.AlterField(
            model_name='blogtranslation',
            name='preview',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='comment',
            name='ip',
            field=models.GenericIPAddressField(default='127.0.0.1'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='language',
            field=models.CharField(choices=[('ru', 'Русский'), ('en', 'English')], default='ru', max_length=5),
        ),
        migrations.AlterField(
            model_name='comment',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='title',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]