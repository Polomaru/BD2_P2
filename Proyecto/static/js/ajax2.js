


function Datos(){

    const xhttp = new XMLHttpRequest();

    xhttp.open('GET','/static/data/rpta.json',true);

    xhttp.send();

    xhttp.onreadystatechange = function(){

        if(this.readyState == 4 && this.status == 200){
            let datos = JSON.parse(this.responseText);
            let res = document.querySelector('#res');
            res.innerHTML = '';

            for(let item of datos){
                res.innerHTML +=`
                <tr>
                <td>${item.username}</td>
                <td>${item.date}</td>
                <td>${item.content}</td>
                <td>${item.url}</td>
                <td>${item.score}</td>
                </tr>
                `;
            }
            $('#lista-twets').DataTable;
        }
    }

}


