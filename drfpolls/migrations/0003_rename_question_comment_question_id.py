# Generated by Django 4.1.7 on 2023-03-28 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drfpolls', '0002_comment_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='question',
            new_name='question_id',
        ),
    ]