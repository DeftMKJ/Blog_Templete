# Generated by Django 2.2.4 on 2019-09-26 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField()),
                ('comment_time', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_comment', to='comment.Comment')),
                ('reply_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to=settings.AUTH_USER_MODEL)),
                ('root', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='root_comment', to='comment.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['comment_time'],
            },
        ),
    ]
