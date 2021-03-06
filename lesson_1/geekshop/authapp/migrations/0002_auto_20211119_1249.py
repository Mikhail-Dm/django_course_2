# Generated by Django 3.2.8 on 2021-11-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activate_key',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Ключ активации'),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='users_avatars', verbose_name='аватар'),
        ),
    ]
