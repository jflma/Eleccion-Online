function cambiarEstadoLista(id_lista, accion) {
    let url = '';
    let metodo = 'PUT';
    let mensajeExito = '';

    if (accion === 'aprobar') {
        url = `/aprobar_lista/${id_lista}`;
        mensajeExito = 'Lista aprobada correctamente';
    } else if (accion === 'desaprobar') {
        url = `/desaprobar_lista/${id_lista}`;
        mensajeExito = 'Lista desaprobada correctamente';
    } else {
        alert('Acción no válida');
        return;
    }

    fetch(url, {
        method: metodo,
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        console.log('HTTP status:', response.status); // Debug: Imprimir el estado HTTP
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text); });
        }
        return response.json().catch(error => {
            console.error('Error parsing JSON:', error); // Debug: Imprimir error de JSON
            throw new Error('La respuesta no es un JSON válido');
        });
    })
    .then(data => {
        console.log('Datos recibidos:', data); // Debug: Imprimir datos recibidos
        alert(mensajeExito);
        location.reload();
    })
    .catch(error => {
        console.error('Error capturado:', error); // Debug: Imprimir errores
        alert('Error al cambiar el estado de la lista');
    });
}
