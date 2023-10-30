# Generated by Django 3.2.13 on 2022-11-04 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_cms_integration', '0037_alter_setting_session_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LangMouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ques_id', models.IntegerField(default=0)),
                ('economy', models.CharField(blank=True, max_length=400)),
                ('care', models.CharField(blank=True, max_length=400)),
                ('technology', models.CharField(blank=True, max_length=400)),
                ('embedding', models.CharField(blank=True, max_length=400)),
                ('law', models.CharField(blank=True, max_length=400)),
                ('ethics', models.CharField(blank=True, max_length=400)),
            ],
        ),
        migrations.AlterField(
            model_name='roles',
            name='session_id',
            field=models.CharField(max_length=10),
        ),
    ]