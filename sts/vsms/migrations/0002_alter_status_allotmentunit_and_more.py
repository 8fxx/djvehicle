# Generated by Django 4.1.4 on 2022-12-15 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vsms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='allotmentunit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statusunit', to='vsms.unit'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='issuedtounit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicleunit', to='vsms.unit'),
        ),
    ]
