# Generated by Django 3.2.9 on 2022-02-28 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_list_app', '0002_auto_20220228_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='platform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='imdb_list_app.streamplatform'),
            preserve_default=False,
        ),
    ]