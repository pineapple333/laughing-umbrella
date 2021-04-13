# Generated by Django 3.2 on 2021-04-13 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authors', models.CharField(max_length=1000)),
                ('title', models.CharField(max_length=256)),
                ('points', models.IntegerField(default=0)),
            ],
        ),
    ]
