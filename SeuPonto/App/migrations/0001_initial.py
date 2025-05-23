# Generated by Django 5.1.7 on 2025-04-03 14:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ponto",
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
                ("entrada", models.DateTimeField(auto_now_add=True)),
                ("saida", models.DateTimeField(blank=True, null=True)),
                ("carga_horaria", models.DurationField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ativo", "Ativo"),
                            ("pausado", "Pausado"),
                            ("finalizado", "Finalizado"),
                        ],
                        default="ativo",
                        max_length=10,
                    ),
                ),
                ("descricao", models.TextField(max_length=100)),
                ("tempo_pausado", models.DurationField(blank=True, null=True)),
                ("ultimo_pausa", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
