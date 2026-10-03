from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Curso(models.Model):
    codigo = models.CharField("Código", max_length=20, unique=True)
    nombre = models.CharField("Nombre", max_length=150)
    creditos = models.PositiveSmallIntegerField(
        "Créditos",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "curso"
        verbose_name_plural = "cursos"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
