let idEditar = null;

window.onload = function () {
    cargarClientes();

    document.getElementById('form-clientes').addEventListener('submit', function (e) {
        e.preventDefault();

        const id = document.getElementById('id').value;
        const nombre = document.getElementById('nombre').value;
        const email = document.getElementById('email').value;
        const telefono = document.getElementById('telefono').value;

        if (modoEditar) {
            fetch(`/clientes/${idEditar}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nombre, email, telefono })
            })
            .then(response => {
                if (!response.ok) throw new Error ("Error al actualizar");
                return response.json();
            })
            .then(() => {
                resetFormulario();
                cargarClientes();
            })
            .catch( error => console.error('Error al actualizar', error));
        } else {
            fetch('/clientes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({id, nombre, email, telefono})
            })
            .then(response => {
                if (!response.ok) throw new Error("Error al Agregar");
                return response.json();
            })
            .catch(error => console.error('Error al agregar:', error));
        }
    });
};

let modoEditar = false;

function cargarClientes() {
    fetch('/clientes')
    .then(response => response.json())
    .then(data => {
        const lista = document.getElementById('lista-clientes');
        lista.innerHTML = '';

        data.forEach(cliente => {
            const item = document.createElement('li');
            item.textContent = `ID: ${cliente.id} - Nombre : ${cliente.nombre} - Email: ${cliente.email} - Telefono: ${cliente.telefono}`;

            // Botón eliminar
            const btnEliminar = document.createElement('button');
            btnEliminar.textContent = 'Eliminar';
            btnEliminar.style.marginLeft = '10px';
            btnEliminar.onclick = () => eliminarCliente(cliente.id);

            // Botón editar
            const btnEditar = document.createElement('button');
            btnEditar.textContent = 'Editar';
            btnEditar.style.marginLeft = '5px';
            btnEditar.onclick = () => prepararEdicion(cliente);

            item.appendChild(btnEliminar);
            item.appendChild(btnEditar);
            lista.appendChild(item);
        });
    })
    .catch(error => console.error('Error al cargar cliente:', error));
}

function eliminarCliente(id) {
    if (!confirm(`¡Eliminar cliente con ID ${id}`)) return;

    fetch(`/clientes/${id}`, { method: 'DELETE' })
        .then(response => {
            if (!response.ok) throw new Error("Error al Eliminar");
            cargarClientes();
        })
        .catch(error => console.error('Error al eliminar cliente:', error));
}

function prepararEdicion(cliente) {
    document.getElementById('id').value = cliente.id;
    document.getElementById('nombre').value = cliente.nombre;
    document.getElementById('email').value = cliente.email;
    document.getElementById('telefono').value = cliente.telefono;

    modoEditar = true;
    idEditar = cliente.id;

    // Cambiar botón
    document.querySelector('#form-carro button[type="submit"]').textContent = "Actualizar Clientes";
}

function resetFormulario() {
    document.getElementById('form-clientes').reset();
    modoEditar = false;
    idEditar = null;
    document.querySelector('#form-clientes button[type="submit"]').textContent = "Agregar Clientes";
}