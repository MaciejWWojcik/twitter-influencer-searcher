# Generated by Django 2.1.3 on 2019-01-22 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweetguru', '0007_auto_20190122_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetauthor',
            name='avatar',
            field=models.CharField(blank=True, max_length=256, null=True),
        )
    ]