# Generated by Django 3.2.13 on 2022-06-26 05:33

from django.db import migrations, models
import django.db.models.deletion
import parler.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20210923_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={},
        ),
        migrations.AlterModelOptions(
            name='blogtranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'blog Translation'},
        ),
        migrations.AlterModelManagers(
            name='blog',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='blogtranslation',
            name='language_code',
            field=models.CharField(db_index=True, max_length=15, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='blogtranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='content.blog'),
        ),
    ]
