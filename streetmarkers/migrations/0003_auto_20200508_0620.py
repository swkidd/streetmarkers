# Generated by Django 3.0.5 on 2020-05-08 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streetmarkers', '0002_auto_20200507_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseMarker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('path', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='streetmarkers.Path')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='streetmarkers.MarkerType')),
            ],
        ),
        migrations.CreateModel(
            name='BasicMarker',
            fields=[
                ('basemarker_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='streetmarkers.BaseMarker')),
                ('infoText', models.TextField()),
            ],
            bases=('streetmarkers.basemarker',),
        ),
        migrations.DeleteModel(
            name='Marker',
        ),
    ]
