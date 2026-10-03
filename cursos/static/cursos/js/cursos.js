document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("curso-form");
  const titulo = document.getElementById("form-titulo");
  const btnGuardar = document.getElementById("btn-guardar");
  const btnCancelar = document.getElementById("btn-cancelar");
  const eliminarForm = document.getElementById("eliminar-form");

  const campos = {
    codigo: form.querySelector("[name=codigo]"),
    nombre: form.querySelector("[name=nombre]"),
    creditos: form.querySelector("[name=creditos]"),
  };

  function modoCrear() {
    form.action = form.dataset.crearUrl;
    form.reset();
    campos.creditos.value = 1;
    titulo.textContent = "Gestión de Curso";
    btnGuardar.textContent = "Guardar";
    btnCancelar.classList.add("d-none");
  }

  // EDITAR: carga los datos de la fila en el formulario y cambia su action.
  document.querySelectorAll(".btn-editar").forEach((btn) => {
    btn.addEventListener("click", () => {
      form.action = btn.dataset.url;
      campos.codigo.value = btn.dataset.codigo;
      campos.nombre.value = btn.dataset.nombre;
      campos.creditos.value = btn.dataset.creditos;
      titulo.textContent = "Editar Curso";
      btnGuardar.textContent = "Actualizar";
      btnCancelar.classList.remove("d-none");
      campos.nombre.focus();
    });
  });

  btnCancelar.addEventListener("click", modoCrear);

  // ELIMINAR: confirmación en el navegador y envío por POST.
  document.querySelectorAll(".btn-eliminar").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (confirm(`¿Eliminar el curso "${btn.dataset.nombre}"?`)) {
        eliminarForm.action = btn.dataset.url;
        eliminarForm.submit();
      }
    });
  });
});
