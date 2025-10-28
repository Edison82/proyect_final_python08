let idEditar = null;

window.onload = function () {
    cargarProveedores();

    document.getElementById('form-proveedores').addEventListener('submit', function (e) {
        e.preventDefault();

        const nombre = document.getElementById('nombre').value;
        const email = document.getElementById('email').value;
        const telefono = document.getElementById('telefono').value;
        const id_legal = document.getElementById('id_legal').value;

        if (modoEditar) {
            fetch(`/proveedores/${idEditar}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nombre, email, telefono, id_legal })
            })
            .then(response => {
                if (!response.ok) throw new Error ("Error al actualizar");
                return response.json();
            })
            .then(() => {
                resetFormulario();
                cargarProveedores();
            })
            .catch( error => console.error('Error al actualizar', error));
        } else {
            fetch('/proveedores', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nombre, email, telefono, id_legal})
            })
            .then(response => {
                if (!response.ok) throw new Error("Error al Agregar");
                return response.json();
            })
            .then(() => {
                resetFormulario();
                cargarProveedores();
            })
            .catch(error => console.error('Error al agregar:', error));
        }
    });
};

let modoEditar = false;

function cargarProveedores() {
    fetch('/proveedores')
    .then(response => response.json())
    .then(data => {
        const lista = document.getElementById('lista-proveedores');
        lista.innerHTML = '';

        data.forEach(proveedor => {
            const item = document.createElement('li');
            item.textContent = `ID: ${proveedor.id} - Nombre : ${proveedor.nombre} - Email: ${proveedor.email} - Telefono: ${proveedor.telefono} - Identificacion Legal: ${proveedor.id_legal}`;

            // Botón eliminar
            const btnEliminar = document.createElement('button');
            btnEliminar.textContent = 'Eliminar';
            btnEliminar.style.marginLeft = '10px';
            btnEliminar.onclick = () => eliminarCliente(cliente.id);

            // Botón editar
            const btnEditar = document.createElement('button');
            btnEditar.textContent = 'Editar';
            btnEditar.style.marginLeft = '5px';
            btnEditar.onclick = () => prepararEdicion(proveedor);

            item.appendChild(btnEliminar);
            item.appendChild(btnEditar);
            lista.appendChild(item);
        });
    })
    .catch(error => console.error('Error al cargar proveedor:', error));
}

function eliminarProveedor(id) {
    if (!confirm(`¡Eliminar proveedor con ID ${id}`)) return;

    fetch(`/proveedores/${id}`, { method: 'DELETE' })
        .then(response => {
            if (!response.ok) throw new Error("Error al Eliminar");
            cargarProveedores();
        })
        .catch(error => console.error('Error al eliminar proveedor:', error));
}

function prepararEdicion(proveedor) {
    document.getElementById('id').value = proveedor.id;
    document.getElementById('nombre').value = proveedor.nombre;
    document.getElementById('email').value = proveedor.email;
    document.getElementById('telefono').value = proveedor.telefono;
    document.getElementById('id_legal').value = proveedor.id_legal;

    modoEditar = true;
    idEditar = proveedor.id;

    // Cambiar botón
    document.querySelector('#form-proveedores button[type="submit"]').textContent = "Actualizar Proveedores";
}

function resetFormulario() {
    document.getElementById('form-proveedores').reset();
    modoEditar = false;
    idEditar = null;
    document.querySelector('#form-proveedores button[type="submit"]').textContent = "Agregar Proveedores";
}