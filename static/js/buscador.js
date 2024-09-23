/*
    tareas pendientes
    buscar que incluya fechas, precios, estrellas/calidad
    Listado de búsqueda que presente fechas, habitaciones, 

*/
let currentPage = 1;
const itemsPerPage = 4;
let filteredAlojamientos = [];
starsValue=0;

function validar(parametro) {
    if (typeof parametro === 'string' && parametro.trim() !== '') {
        console.log('El parámetro tiene un valor válido:', parametro);
        return parametro
    } else {
        console.log('localidad convertida a cadena vacia');
        let parametro = '';
        return '';
    }
}
function busquedaPrincipal() {

    filteredAlojamientos = [];
    let existeM = document.getElementById("destino");
    let municipio = new String(validar(existeM.options[existeM.selectedIndex].value)).toLowerCase();
    let nombrew = new String(validar(document.getElementById("nombreA").value)).toLowerCase();

    if (nombrew == '' && municipio == '') {
        alert('introduzca el nombre de un hotel o de un municipio')
        return;
    }
    //incluir la validación de fechas
    //incluir la validacion de estrellas
    //incluir la validación de precios
    
    var allAlojamiento = []

    lecturaXML('alojamientos.xml', 'Alojamientos');

    try{buscar(Alojamientos.hoteles.hotel, nombrew, municipio);}catch(error){};
    try{buscar(Alojamientos.hostales.hostal, nombrew, municipio);}catch(error){};
    try{buscar(Alojamientos.campings.camping, nombrew, municipio);}catch(error){};
    try{buscar(Alojamientos.apartamentos.apartamento, nombrew, municipio);}catch(error){};

    displayResults(filteredAlojamientos);

    // Desplazar la página hasta los resultados
    const resultsContainer = document.getElementById("results");
    if (resultsContainer) {
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}
function buscar(alojamientoB, nombre, municipio) {

    document.getElementById("results").innerHTML = "";
    document.getElementById("pagination").innerHTML = "";
    
    const arrivalDate = $("#startDate").datepicker('getDate').toLocaleDateString();
    console.log(arrivalDate);
    const departureDate = $("#endDate").datepicker('getDate').toLocaleDateString();
    console.log(departureDate);
    const pricemin = $("#price-slider").slider("values", 0);
    console.log(pricemin);
    const pricemax=$("#price-slider").slider("values", 1);
    console.log(pricemax);
    const person=$("#person-count").val();
    console.log(person);
    const room= $("#room-count").val();
    console.log(room);
    const estrella =starsValue;
    console.log(starsValue);

  

    let nombre_A = new String("");
    let municipio_A = new String("");
    
    /*let precio_A = new String("");

    let estrella_A = new String("");*/



    //try{
    alojamientoB.forEach(alojamiento => {

        let resultadoF=false;
        let municipio_ = new RegExp(municipio);
        let nombre_ = new RegExp(nombre);
        municipio_A = alojamiento.attributes.poblacion.toLowerCase();
        nombre_A = alojamiento.nombre.toLowerCase();
       /* let precio_=new RegExp(price);
        let estrella_= new RegExp(estrella);
        precio_A = parseFloat(alojamiento.getAttribute("precio"));
        estrella_A = parseInt(alojamiento.getAttribute("estrellas"));
        
        if (precio_A >= pricemin && precio_A <= pricemax) {
            {resultadoF = true;}
        } else {
            console.log("Con este rango, no existe ningún precio.");
        }
        */
        if(municipio_.test(municipio_A)&&nombre_.test(nombre_A))
            {resultadoF=true;}
        else if(municipio_.test(municipio_A)&&nombre=='')
            {resultadoF=true;}
        else if(nombre_.test(nombre_A)&&municipio=='')
            {resultadoF=true;}

//añadir fechas
//añadir estrellas, compatibilizar los diferentes
//añadir precio

        if ((resultadoF)) {
            filteredAlojamientos.push({
                name: alojamiento.nombre,
                price: alojamiento.attributes.precio,
                //arrival: arrival,
                //departure: departure,
                stars: alojamiento.attributes.estrellas,
                available: alojamiento.attributes.habitaciones
            });
        }
        /*});}
        catch(error)
        {}*/
        /*try {
            alojamientoB.forEach(alojamiento => {
                var expresionRegular = new RegExp(nombreHotel);
                var resultado = expresionRegular.test(alojamiento.nombre.toLowerCase());
    
                if (resultado) {
                    filteredAlojamientos.push({
                        name: alojamiento.nombre,
                        price: alojamiento.attributes.precio,
                        //arrival: arrival,
                        //departure: departure,
                        stars: alojamiento.attributes.estrellas,
                        available: alojamiento.attributes.habitaciones
                    });
                }
            });
        } catch (error) {
            var expresionRegular = new RegExp(nombreHotel);
            var resultado = expresionRegular.test(alojamientoB.nombre.toLowerCase());
    
            if (resultado) {
                filteredAlojamientos.push({
                    name: alojamientoB.nombre,
                    price: alojamientoB.attributes.precio,
                    //arrival: arrival,
                    //departure: departure,
                    stars: alojamientoB.attributes.estrellas,
                    available: alojamientoB.attributes.habitaciones
                });
            }
        }*/

    });
}


function displayResults(alojamientos) {
    const resultsContainer = document.getElementById("results");
    const loadingIndicator = document.getElementById("loadingIndicator");
    loadingIndicator.style.display = "block";

    setTimeout(function() {
        resultsContainer.innerHTML = "";
        resultsContainer.style.padding="20px";
        loadingIndicator.style.display = "none";
        resultsContainer.style.fontSize = "large";


        if (alojamientos.length === 0) {
            resultsContainer.textContent = "No se encontraron alojamientos que coincidan con los criterios de búsqueda.";
        
        
        } else {
            const totalPages = Math.ceil(alojamientos.length / itemsPerPage);
            const startIndex = (currentPage - 1) * itemsPerPage;
            const endIndex = startIndex + itemsPerPage;

            const table = document.createElement("table");
            table.classList.add("table", "table-striped", "custom-table");

            const headerRow = document.createElement("tr");
            headerRow.innerHTML = `
                <th>Nombre</th>
                <th>Precio</th>
                <th>Fecha de llegada</th>
                <th>Fecha de salida</th>
                <th>Disponibilidad</th>
                <th>Estrellas</th>
                <th></th> <!-- Columna para el botón de ir al alojamiento -->
            `;
            table.appendChild(headerRow);

            for (let i = startIndex; i < endIndex && i < alojamientos.length; i++) {
                const alojamiento = alojamientos[i];
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${alojamiento.name}</td>
                    <td>${alojamiento.price}</td>
                    <td>${$("#startDate").datepicker('getDate').toLocaleDateString()}</td>
                    <td>${$("#endDate").datepicker('getDate').toLocaleDateString()}</td>
                    <td>${alojamiento.available ? '<i class="fas fa-check-circle"></i>' : '<i class="fas fa-times-circle"></i>'}</td>
                    <td>${getStars(alojamiento.stars)}</td>
                    <td><button onclick="window.location.href='/alojamiento/${alojamiento.name}'"><i class="fas fa-hotel"></i> Ir al alojamiento</button></td>
                `;
                table.appendChild(row);
            }

            resultsContainer.appendChild(table);

            const paginationContainer = document.getElementById("pagination");
            paginationContainer.innerHTML = "";

            const prevButton = document.createElement("button");
            prevButton.textContent = "Anterior";
            prevButton.addEventListener("click", () => {
                if (currentPage > 1) {
                    currentPage--;
                    displayResults(alojamientos);
                }
            });
            paginationContainer.appendChild(prevButton);

            const pageInfo = document.createElement("span");
            pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
            paginationContainer.appendChild(pageInfo);

            const nextButton = document.createElement("button");
            nextButton.textContent = "Siguiente";
            nextButton.addEventListener("click", () => {
                if (currentPage < totalPages) {
                    currentPage++;
                    displayResults(alojamientos);
                }
            });
            paginationContainer.appendChild(nextButton);
        }
    }); 
}


function resetSearchForm() {
    document.getElementById("destino").value = "";
    document.getElementById("pagination").innerHTML = "";
    document.getElementById("results").innerHTML = "";
    document.getElementById("nombre").value = "";
    document.getElementById("arrival").value = "";
    document.getElementById("departure").value = "";
    document.getElementById("min-price").value = "";
    document.getElementById("max-price").value = "";
    currentPage = 1;
    //document.getElementById("search-form").submit();
}
function getStars(numStars) {
    let stars = '';
    for (let i = 0; i < numStars; i++) {
        stars += '<i class="fas fa-star"></i>';
    }
    return stars;
}
