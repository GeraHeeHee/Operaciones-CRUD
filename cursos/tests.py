from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .models import Curso


def datos(**extra):
    base = {"codigo": "425672", "nombre": "Programación Avanzada III", "creditos": 8}
    base.update(extra)
    return base


class ModeloCursoTests(TestCase):
    def test_str(self):
        curso = Curso.objects.create(**datos())
        self.assertEqual(str(curso), "425672 - Programación Avanzada III")

    def test_codigo_unico(self):
        Curso.objects.create(**datos())
        with self.assertRaises(IntegrityError), transaction.atomic():
            Curso.objects.create(**datos(nombre="Otro"))


class ReadTests(TestCase):
    def test_lista_vacia(self):
        resp = self.client.get(reverse("cursos:lista"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "No hay cursos registrados.")
        self.assertContains(resp, "¡Cursos listados!")

    def test_lista_muestra_cursos(self):
        Curso.objects.create(**datos())
        Curso.objects.create(codigo="924129", nombre="Fundamentos de Diseño Web", creditos=5)
        resp = self.client.get(reverse("cursos:lista"))
        self.assertEqual(resp.context["cursos"].count(), 2)
        self.assertContains(resp, "Programación Avanzada III")
        self.assertContains(resp, "Fundamentos de Diseño Web")


class CreateTests(TestCase):
    def test_crear_valido(self):
        resp = self.client.post(reverse("cursos:crear"), datos())
        self.assertRedirects(resp, reverse("cursos:lista"))
        self.assertEqual(Curso.objects.count(), 1)
        self.assertEqual(Curso.objects.get().creditos, 8)

    def test_crear_codigo_duplicado(self):
        Curso.objects.create(**datos())
        self.client.post(reverse("cursos:crear"), datos(nombre="Otro"))
        self.assertEqual(Curso.objects.count(), 1)

    def test_crear_creditos_invalidos(self):
        for valor in (0, 21, -3, "abc"):
            self.client.post(reverse("cursos:crear"), datos(creditos=valor))
        self.assertEqual(Curso.objects.count(), 0)

    def test_crear_campos_vacios(self):
        self.client.post(reverse("cursos:crear"), {"codigo": "", "nombre": "", "creditos": ""})
        self.assertEqual(Curso.objects.count(), 0)

    def test_crear_no_acepta_get(self):
        resp = self.client.get(reverse("cursos:crear"))
        self.assertEqual(resp.status_code, 405)


class UpdateTests(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(**datos())

    def test_editar_valido(self):
        url = reverse("cursos:editar", args=[self.curso.pk])
        resp = self.client.post(url, datos(nombre="Lenguaje", creditos=4))
        self.assertRedirects(resp, reverse("cursos:lista"))
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.nombre, "Lenguaje")
        self.assertEqual(self.curso.creditos, 4)

    def test_editar_invalido_no_cambia(self):
        url = reverse("cursos:editar", args=[self.curso.pk])
        self.client.post(url, datos(creditos=0))
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.creditos, 8)

    def test_editar_codigo_duplicado(self):
        otro = Curso.objects.create(codigo="348942", nombre="Lenguaje", creditos=4)
        url = reverse("cursos:editar", args=[otro.pk])
        self.client.post(url, datos(nombre="Lenguaje"))  # intenta usar 425672
        otro.refresh_from_db()
        self.assertEqual(otro.codigo, "348942")

    def test_editar_inexistente(self):
        resp = self.client.post(reverse("cursos:editar", args=[999]), datos())
        self.assertEqual(resp.status_code, 404)


class DeleteTests(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(**datos())

    def test_eliminar(self):
        resp = self.client.post(reverse("cursos:eliminar", args=[self.curso.pk]))
        self.assertRedirects(resp, reverse("cursos:lista"))
        self.assertFalse(Curso.objects.filter(pk=self.curso.pk).exists())

    def test_eliminar_no_acepta_get(self):
        resp = self.client.get(reverse("cursos:eliminar", args=[self.curso.pk]))
        self.assertEqual(resp.status_code, 405)
        self.assertEqual(Curso.objects.count(), 1)

    def test_eliminar_inexistente(self):
        resp = self.client.post(reverse("cursos:eliminar", args=[999]))
        self.assertEqual(resp.status_code, 404)
