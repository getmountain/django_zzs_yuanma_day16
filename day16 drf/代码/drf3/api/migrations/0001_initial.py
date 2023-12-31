# Generated by Django 3.2 on 2022-10-02 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('token', models.CharField(blank=True, db_index=True, max_length=64, null=True, verbose_name='TOKEN')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(choices=[(1, '云计算'), (2, 'Python全栈'), (3, 'Go开发')], verbose_name='分类')),
                ('image', models.CharField(max_length=255, verbose_name='封面')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('summary', models.CharField(max_length=256, verbose_name='简介')),
                ('text', models.TextField(verbose_name='博文')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('comment_count', models.PositiveIntegerField(default=0, verbose_name='评论数')),
                ('favor_count', models.PositiveIntegerField(default=0, verbose_name='赞数')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo', verbose_name='创建者')),
            ],
        ),
    ]
