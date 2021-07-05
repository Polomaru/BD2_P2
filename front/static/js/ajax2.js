


function Datos(){

    const xhttp = new XMLHttpRequest();

    xhttp.open('GET','../tweets_2021-06-22.json',true);

    xhttp.send();

    xhttp.onreadystatechange = function(){

        if(this.readyState == 4 && this.status == 200){
            let datos = JSON.parse(this.responseText);
            let res = document.querySelector('#res');
            res.innerHTML = '';

            for(let item of datos){
                res.innerHTML +=`
                <tr>
                <td>${item.id}</td>
                <td>${item.date}</td>
                <td>${item.text}</td>
                <td>${item.user_name}</td>
                </tr>
                `;
            }
            $('#lista-twets').DataTable;
        }
    }

}


