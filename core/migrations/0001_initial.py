# Generated by Django 2.1.2 on 2018-10-08 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('jackpot', models.DecimalField(decimal_places=2, max_digits=13)),
                ('winners', models.IntegerField()),
            ],
            options={
                'db_table': 'draw',
            },
        ),
        migrations.CreateModel(
            name='DrawBall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.IntegerField(max_length=2)),
                ('order', models.IntegerField(max_length=1)),
                ('draw', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Draw')),
            ],
            options={
                'db_table': 'draw_table',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('digits', models.IntegerField(default=6)),
                ('max_digit', models.IntegerField(default=58)),
            ],
            options={
                'db_table': 'game',
            },
        ),
        migrations.AddField(
            model_name='draw',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Game'),
        ),
    ]
