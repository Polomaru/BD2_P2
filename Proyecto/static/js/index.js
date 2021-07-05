const tabla = document.querySelector('#lista-twets tbody');

function cargartwets() {
    fetch('/static/tweets_2021-06-22.json')
        .then(respuesta => respuesta.json())
        .then(salida => {
            salida.forEach(salida => {
                const row = document.createElement('tr');
                row.innerHTML += `
                    <td>${salida.id}</td>
                    <td>${salida.date}</td>
                    <td>${salida.text}</td>
                    <td>${salida.user_name}</td>
                `;
                tabla.appendChild(row);

            });
            row.DataTable();
        })
        .catch(error => console.log('Se produjo un error ' + error.message))

        $('#lista-twets').DataTable;
}


cargartwets();


