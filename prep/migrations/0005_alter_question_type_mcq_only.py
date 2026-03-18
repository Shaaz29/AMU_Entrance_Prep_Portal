from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prep', '0004_userprofile_photo_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(default='MCQ', editable=False, max_length=3),
        ),
    ]
