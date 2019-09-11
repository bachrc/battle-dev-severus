# Generated by Django 2.2.3 on 2019-09-07 19:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('lobby', '0003_battledev'),
    ]

    operations = [
        migrations.AddField(
            model_name='probleme',
            name='image',
            field=models.ImageField(default='oui', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='battledev',
            name='description',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='probleme',
            name='contenu',
            field=models.TextField(max_length=10000),
        ),
    ]