# Generated by Django 4.1.1 on 2024-12-16 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('notifications', '0006_user_groups_user_is_staff_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationstring',
            name='text',
            field=models.TextField(default=4, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='translationstring',
            unique_together={('content_type', 'object_id', 'language')},
        ),
    ]
