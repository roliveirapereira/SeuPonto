# Generated by Django 5.1.7 on 2025-04-04 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("App", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ponto",
            name="tempo_pausado",
        ),
        migrations.RemoveField(
            model_name="ponto",
            name="ultimo_pausa",
        ),
        migrations.AddField(
            model_name="ponto",
            name="anotacao_tecnica",
            field=models.CharField(default="Null", max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="ponto",
            name="status",
            field=models.CharField(
                choices=[("ativo", "Ativo"), ("finalizado", "Finalizado")],
                default="ativo",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="Pausa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("inicio", models.DateTimeField(auto_now_add=True)),
                ("fim", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(default="ativo", max_length=10)),
                (
                    "ponto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pausas",
                        to="App.ponto",
                    ),
                ),
            ],
        ),
    ]
