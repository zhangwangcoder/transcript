# Generated by Django 3.0.2 on 2020-03-13 08:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('audio', models.FileField(upload_to='audios/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('speaker_num', models.PositiveIntegerField(default=1)),
                ('language', models.CharField(default='en-US', max_length=20)),
                ('model', models.CharField(choices=[('video', 'Video'), ('phone_call', 'Phone Call')], default='video', help_text='select to enhance recognition result', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, null=True)),
                ('password', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript', models.FileField(upload_to='transcripts/')),
                ('audio', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Audio')),
            ],
        ),
    ]
