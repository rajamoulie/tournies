# Generated by Django 4.0.2 on 2022-02-04 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Tourney',
        ),
    ]