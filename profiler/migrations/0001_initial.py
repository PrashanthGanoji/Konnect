# Generated by Django 2.0.6 on 2018-07-22 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=128)),
                ('school', models.CharField(max_length=128)),
                ('location', models.CharField(max_length=256)),
                ('fieldOfStudy', models.CharField(max_length=128)),
                ('start', models.DateField()),
                ('end', models.DateField(blank=True, null=True)),
                ('description', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('company', models.CharField(max_length=128)),
                ('location', models.CharField(max_length=256)),
                ('start', models.DateField()),
                ('end', models.DateField(blank=True, null=True)),
                ('current', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('hasimg', models.BooleanField(default=False)),
                ('img', models.ImageField(blank=True, null=True, upload_to='posts/')),
                ('description', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handel', models.CharField(max_length=128)),
                ('fullname', models.CharField(max_length=512)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('location', models.CharField(max_length=128)),
                ('website', models.URLField(blank=True, max_length=256, null=True)),
                ('status', models.CharField(max_length=128)),
                ('bio', models.CharField(max_length=512)),
                ('linkedIn', models.URLField(blank=True, max_length=512, null=True)),
                ('gitusername', models.CharField(max_length=128)),
                ('friends', models.ManyToManyField(related_name='_profile_friends_+', to='profiler.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='profiler.Skills'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='posts',
            name='likes',
            field=models.ManyToManyField(related_name='posts_likes', to='profiler.Profile'),
        ),
        migrations.AddField(
            model_name='posts',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiler.Profile'),
        ),
        migrations.AddField(
            model_name='posts',
            name='tags',
            field=models.ManyToManyField(to='profiler.Tags'),
        ),
        migrations.AddField(
            model_name='experience',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiler.Profile'),
        ),
        migrations.AddField(
            model_name='education',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiler.Profile'),
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiler.Posts'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiler.Profile'),
        ),
    ]
