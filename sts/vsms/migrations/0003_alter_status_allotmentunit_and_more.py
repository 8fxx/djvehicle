# Generated by Django 4.1.4 on 2022-12-15 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vsms', '0002_alter_status_allotmentunit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='allotmentunit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unit', to='vsms.unit'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='issuedtounit',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
