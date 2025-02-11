# Generated by Django 3.0.5 on 2020-05-10 11:06

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
            name='Peg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PegType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BasicPeg',
            fields=[
                ('peg_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pegs.Peg')),
                ('encoded', models.CharField(max_length=30)),
            ],
            bases=('pegs.peg',),
        ),
        migrations.CreateModel(
            name='PAOPeg',
            fields=[
                ('peg_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pegs.Peg')),
                ('person', models.CharField(max_length=30)),
                ('action', models.CharField(max_length=30)),
                ('object', models.CharField(max_length=30)),
            ],
            bases=('pegs.peg',),
        ),
        migrations.CreateModel(
            name='POPeg',
            fields=[
                ('peg_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pegs.Peg')),
                ('person', models.CharField(max_length=30)),
                ('object', models.CharField(max_length=30)),
            ],
            bases=('pegs.peg',),
        ),
        migrations.CreateModel(
            name='PegSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='peg',
            name='pegSystem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pegs.PegSystem'),
        ),
        migrations.AddField(
            model_name='peg',
            name='pegType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pegs.PegType'),
        ),
    ]
