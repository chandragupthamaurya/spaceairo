# Generated by Django 3.2.2 on 2021-05-30 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0011_auto_20210530_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='adminchoose',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]