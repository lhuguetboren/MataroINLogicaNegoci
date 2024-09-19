var hotelData=[]
var controlCargado=0
//funciones del buscador

function buscadorEstrellas(){
    // Aquí puedes implementar la lógica para procesar la búsqueda con los valores ingresados en el formulario

    // Ejemplo de cómo acceder a los valores ingresados en el formulario:
    const formData = new FormData(this);
    const municipio = formData.get('municipioInput');
    const hotel = formData.get('hotelInput');
    const tipoA = formData.get('tipoAInput');


    const habitantesMin = formData.get('habitantesMinInput');
    const habitantesMax = formData.get('habitantesMaxInput');
    const estrellas = formData.get('estrellasInput');
    const calidad = formData.get('calidadInput');
    const servicios = formData.get('serviciosInput');

    // Aquí puedes realizar la búsqueda con los valores obtenidos y mostrar los resultados
    console.log('Municipio:', municipio);
    console.log('tipo Alojamiento:', tipoA);

    console.log('hotel:', hotel);
    console.log('Habitantes mínimos:', habitantesMin);
    console.log('Habitantes máximos:', habitantesMax);
    console.log('Número de estrellas:', estrellas);
    console.log('Calidad del hostal:', calidad);
    console.log('Servicios en el camping:', servicios);

    buscar_por_municipio(municipio, hotel, estrellas,tipoA,calidad);

    // Por ahora, solo mostramos los valores en la consola. Debes implementar la lógica de búsqueda y visualización de resultados.
};
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
function buscar_por_municipio(localidad, hotel, estrellasF, tipoA,calidad) {
    localidad = validar(localidad);
    tipoA = validar(tipoA);
    calidad=validar(calidad);
    var salidaTexto='';


    for (i = 0; i < municipios.length - 1; i++) {
        if (municipios[i].nombre.toLowerCase() == localidad.toLowerCase() || localidad == '') {

            if (tipoA == 'hoteles'||tipoA=='') {
                for (k = 0; k < municipios[i].hoteles.length - 1; k++) {
                    {if (municipios[i].hoteles[k].estrellas == estrellasF||estrellasF==0) 
                    { 
                        //console.log('Estoy en el hotel' + municipios[i].hoteles[k].nombre); 
                        //salidaTexto+='<p>'+municipios[i].hoteles[k].nombre + '</p>';
                        crearElementoListado(municipios[i].hoteles[k].nombre)

                }
                }}
            }
            if (tipoA == 'campings'||tipoA=='') {
                for (k = 0; k < municipios[i].campings.length - 1; k++) {
                    { 
                        //console.log('Estoy en el camping' + municipios[i].campings[k].nombre); 
               
                    //salidaTexto+='<p>'+municipios[i].campings[k].nombre + '</p>';
                    crearElementoListado(municipios[i].campings[k].nombre)


                }         
                }                      
            
            }
            if (tipoA == 'hostales'||tipoA=='') 
            {
                for (k = 0; k < municipios[i].hostales.length - 1; k++) {
                    {if (municipios[i].hostales[k].calidad == calidad||calidad=='') 

                    { 
                        //console.log('Estoy en el hostales' + municipios[i].hostales[k].nombre); 
                        //salidaTexto+='<p>'+municipios[i].hostales[k].nombre + '</p>';}
                        crearElementoListado(municipios[i].hostales[k].nombre)


                    }

                    }
                }

            }

        }
}

}
function crearElementoListado(texto)

    {
        var divLinea = document.createElement("div");
        divLinea.style.width="100%";
        divLinea.style.height="50px";
        var para = document.createElement("p");
        para.style.width="30%";
        para.style.float="left";
        para.innerHTML = texto;
        var icono = document.createElement("img");
        icono.src="https://trainingtutor.net/IFCD0210_CEN/CGPP/MataroIN/assets/imagenes/logoNEGATIVO.png"
        icono.style.width="100px";
        icono.style.float="left";
        var enlaceHotel = document.createElement('a');
        //enlaceHotel.href=texto;
        enlaceHotel.setAttribute('onclick','interaccion("'+texto +'","ocupado")');
        enlaceHotel.style.cursor="pointer";

        enlaceHotel.appendChild(icono)
        divLinea.appendChild(para);
        divLinea.appendChild(enlaceHotel);
        document.getElementById("salida").appendChild(divLinea);

    }
function interaccion(hotel,estado)
{
    switch(estado) {
        case 'libre':
            window.open('alojamiento2.html?hotel='+hotel);
            break;
        case 'ocupado':
            alert("Alojamiento ocupado, vea el alojamiento")
            window.open('alojamiento2.html?hotel='+hotel);
            break;
        case 'cerrado':
            alert("Alojamiento cerrado, seleccione otro")

        default:
            // code block
        } 



}




function CargaAlojamiento(controlC)
{
if(controlC==1) return;
//Lectura 

for(i=0;i<Alojamientos.hoteles.hotel.length;i++)
{
    if(Alojamientos.hoteles.hotel[i].nombre.toLowerCase()==controlC.toLowerCase()) break;
  
}
let hotelData=Alojamientos.hoteles.hotel[i]


//presentacion
RecuperaCadena("hotel", hotelData.nombre, 'html');
RecuperaCadena("direccion", hotelData.direccion, 'html');
RecuperaCadena("imagen", hotelData.imagen, 'img');
RecuperaCadena("descripcion", hotelData.descripcion, 'html');
RecuperaCadena("correo", hotelData.correo, 'html');
RecuperaCadena("telefono", hotelData.telefono, 'html');




document.getElementById("servicios").innerHTML = '<h2>Servicios</h2>';
// Ejemplo de arreglo que contiene las claves del mapa
 
asservicios=hotelData.servicios.split(',');
 
let cadena = "";

for (let i = 0; i < asservicios.length; i++) {

  cadena += `<img id="`+asservicios[i].trim()+`" class="icono" src="static/imagenes/`+serviciosIMG.get(asservicios[i].trim())+`" width="20px" height="20px"
  onmouseover="mostrarMensaje (this.id)" onmouseout="ocultarMensaje()">`
}

document.getElementById("servicios").innerHTML=cadena;
/*img source=
console.log(cadena); // Imprime la cadena con las rutas de las imágenes

//AJUSTE 3
//Presentar por mes los dias libres

/*Inserto por texto en el contendio del div un título*/


document.getElementById("fechas").innerHTML = '<h2>Fechas</h2>';



//Obtengo del objeto javascript las cadena de los meses
//creo un array temporal
var arrayMeses = []
let claves= Object.keys(hotelData.fechas)
for (i = 0; i <claves.length; i++) {
    //inserto en el array la cadena del mes, la i recorre los registros existentes, el 0 indica que es el primer elemento de fecha
    arrayMeses.push(claves[i]);
}
console.log(arrayMeses)
//inserto un child en el div fechas con un desplegable con los meses existentes
document.getElementById("fechas").appendChild(crearSelect(arrayMeses));
//inserto un child en el div fechas con los datos de dias y plaas libres de enero
document.getElementById("fechas").appendChild(crearTable(hotelData,"enero",0));



// Definir el valor constante
let Precio = hotelData.attributes.precio;
document.getElementById("precio").innerHTML = '<h2>Precios</h2>';
document.getElementById("precio").innerHTML += '<p> El precio de una plaza por persona es ' + Precio + '</p><h3>Ofertas</h3>';
document.getElementById("precio").innerHTML += '<p><div style="width:35%;float:left;">Descuento</div>';
document.getElementById("precio").innerHTML += '<div style="width:25%;float:left;">Noches</div>';
document.getElementById("precio").innerHTML += '<div style="width:25%;float:left;">Total</div></p>';


let objetoOfertas = document.getElementById("ofertas")
document.getElementById("servicios").innerHTML += cadena;

// Bucle que va desde 1 hasta 4
for (let i = 2; i <= 4; i++) {
    linea = document.createElement('p');
    linea.style.width = "100%";
    linea.style.display = "flex";

    elementoL = document.createElement('div');
    elementoL.style.width = "35%";
    //elementoL.style.display="block";
    elementoL.innerHTML = (i * 10) + '%';
    linea.appendChild(elementoL);
    elementoL = document.createElement('div');
    elementoL.style.width = "25%";
    //elementoL.style.display="block";
    elementoL.innerHTML = i;
    linea.appendChild(elementoL);
    elementoL = document.createElement('div');
    //elementoL.style.width="25%";
    //elementoL.style.display="block";
    elementoL.innerHTML = Precio - (Precio * (i / 10));
    linea.appendChild(elementoL);
    objetoOfertas.appendChild(linea);
}
controlCargado=1;
}



//Al actualizar el desplegable actualizo los datos de la tabla
function ActualizarTable(mes,posicion)
{
    //elimino la tabla anterior
document.getElementById("tableFecha").remove();
//cargo datos
let hotelData=Alojamientos.hoteles.hotel[0]

//creo de nuevo la tabla
document.getElementById("fechas").appendChild(crearTable(hotelData,mes,posicion));
}

//creo la tabla
function crearTable(hotelData) {
    // Crear el elemento select
    //Primero cojo los datos de fechas, [posicion] me indica el registro, 
    //[mes] el nombre de la clave y [0] el primer elemento de esta clave

    console.log(hotelData.fechas);
    fechasSeparadas = hotelData.fechas.split(",");
    hxfSeparadas = hotelData.fechaxhabitaciones.split(",");
    
    //creo los diferentes tags para generar dinamicamente la tabla
    table = document.createElement("table");
    //introduzco un id para poder trabajar con la tabla posteriormente
    table.setAttribute("id", "tableFecha");
    //creo una cabecera
    thead = document.createElement("thead");
    td = document.createElement("td")
    td.innerHTML = "Dia";
    thead.appendChild(td);
    td = document.createElement("td")
    td.innerHTML = "Plazas libres";
    thead.appendChild(td);
    table.appendChild(thead);

    //creo tantas lineas como dias existentes y recupero el numro del día y las plazas libres.

    for (i = 0; i < fechasSeparadas.length; i++) {
        tr = document.createElement("tr");
        td = document.createElement("td");
        td.innerHTML = fechasSeparadas[i]
        tr.appendChild(td)
        td = document.createElement("td");
        td.innerHTML = hxfSeparadas[i]
        tr.appendChild(td)
        td = document.createElement("td");
        tr.appendChild(td)
        table.appendChild(tr)
    }



    // Devolver el tabla creada
    return table;
}

function crearSelect(valores) {
    // Crear el elemento select
    const select = document.createElement("select");
    //creo un atributo onchange para cada vez que cambie el select envie el item seleccionado y el número de orden
    select.setAttribute("onchange","ActualizarTable(this.value,this.selectedIndex);");
        // Iterar sobre los valores y crear opciones para cada uno
        valores.forEach(valor => {
            // Crear opción
            const opcion = document.createElement("option");
            // Asignar el valor a la opción
            opcion.value = valor;
            // Asignar el texto visible a la opción
            opcion.textContent = valor;
            // Agregar la opción al select
            select.appendChild(opcion);
        });

    // Devolver el select creado
    return select;
}

function RecuperaCadena(hotelP, valorP, atributoP) {
    objeto = document.getElementById(hotelP);
    if (atributoP == 'img') {
        objeto.src = valorP;
    }
    else {
        objeto.innerHTML = valorP;
    }
}








