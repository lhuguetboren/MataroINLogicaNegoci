var archiv = 0;
var cargadosDatos = false;


function xmlToObj(xml) {
    const obj = {};

    if (xml.nodeType === 1) { // Nodo de elemento
        if (xml.attributes.length > 0) {
            obj.attributes = {};
            for (let j = 0; j < xml.attributes.length; j++) {
                const attribute = xml.attributes.item(j);
                obj.attributes[attribute.nodeName] = attribute.nodeValue;
            }
        }
        if (xml.hasChildNodes()) {
            let childTextNodes = [];
            for (let i = 0; i < xml.childNodes.length; i++) {
                const item = xml.childNodes.item(i);
                const nodeName = item.nodeName;
                if (item.nodeType === 1) { // Nodo de elemento
                    if (typeof obj[nodeName] === "undefined") {
                        obj[nodeName] = xmlToObj(item);
                    } else {
                        if (typeof obj[nodeName].push === "undefined") {
                            const old = obj[nodeName];
                            obj[nodeName] = [];
                            obj[nodeName].push(old);
                        }
                        obj[nodeName].push(xmlToObj(item));
                    }
                } else if (item.nodeType === 3 && item.nodeValue.trim() !== '') { // Nodo de texto
                    childTextNodes.push(item.nodeValue.trim());
                }
            }
            if (Object.keys(obj).length === 0 && childTextNodes.length === 1) {
                return childTextNodes[0];
            }
        }
        return obj;
    }
}

function objToJson(obj) {
    return JSON.stringify(obj, null, 2);
}

function lecturaXML(url, nombre) {// Utilizar fetch para obtener el archivo XML
    fetch('/static/xml/' + url)
        .then(response => response.text())
        .then(data => {
            // Parsear el XML
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(data, "text/xml");
            // Convertir XML a objeto JavaScript
            const objeto = xmlToObj(xmlDoc.documentElement);

            //asignar a objeto javascript y objetoJson
            switch (nombre) {
                case 'Blog':
                    Blog = objeto;
                    BlogJson = objToJson(objeto);
                    break;
                case 'Municipios':
                    Municipios = objeto;
                    MunicipiosJson = objToJson(objeto);
                    break;
                case 'Alojamientos':
                    Alojamientos = objeto;
                    AlojamientosJson = objToJson(objeto);
                    break;
                case 'Transportes':
                    Transportes = objeto;
                    TransportesJson = objToJson(objeto);
                    break;
                case 'Idiomas':
                    Idiomas = objeto;
                    IdiomasJson = objToJson(objeto);
                    break;
                case 'Biblioteca':
                    Biblioteca = objeto;
                    BibliotecaJson = objToJson(objeto);
                    break;
                case 'Clientes':
                    Clientes = objeto;
                    ClientesJson = objToJson(objeto);
                    break;
                case 'Proveedores':
                    Proveedores = objeto;
                    ProveedoresJson = objToJson(objeto);
                    break;
                case 'Videos':
                        Videos = objeto;
                        VideosJson = objToJson(objeto);
                        break;
                default:


            }
            if (archiv++ == archivos.length) cargadosDatos = true;



        })
        .catch(error => console.error('Error al obtener el archivo XML:', error));


}

function renderizarElemento(elemento, nombre, nivel) {

    if (nivel == 0) {
        let div = document.createElement('div');
        div.className = "tituloArchivo";
        div.style.float = "left";
        div.textContent = nombre.toUpperCase();
        contenedor.appendChild(div);
    };
    if (typeof elemento === 'object' && !Array.isArray(elemento)) {
        for (let clave in elemento) {
            let div = document.createElement('div');
            div.style.float = "left";
            div.className = "tituloCampo";
            div.style.marginLeft = `${nivel * 20}px`;
            div.textContent = `${clave}:`;
            contenedor.appendChild(div);
            renderizarElemento(elemento[clave], contenedor, nivel + 1);
        }
    } else if (Array.isArray(elemento)) {
        elemento.forEach((item) => {
            renderizarElemento(item, contenedor, nivel);
        });
    } else {
        let div = document.createElement('div');
        div.style.marginLeft = `${nivel * 20}px`;
        div.style.float = "left";
        div.className = "valorCampo";
        div.textContent = elemento;
        contenedor.appendChild(div);

    }
}



// Función asíncrona simulada que resuelve después de 1 segundo
async function fetchData() {
    return new Promise(resolve => {
        archivos.forEach((elemento) => {
            setTimeout(() => {
                resolve(lecturaAsync(elemento["archivo"], elemento["nombre"])); // Devuelve un valor aleatorio después de 1 segundo
            }, 1000);
        });
    });
}

function lecturaAsync(a, b) {
    lecturaXML(a, b);
    return archiv;
}
// Función para verificar la condición de salida
function shouldStopFetching(data) {
    return data == 11; // Condición de ejemplo: detenerse si el valor es mayor que 0.8
}

 // Función para cargar todos los datos
 async function cargarDatos() {
    archivos.forEach((elemento) => {
        lecturaXML(elemento["archivo"], elemento["nombre"]);
    });
    const data = await fetchData();
    if (shouldStopFetching(data)) {
        clearInterval(intervalId);
        main();
    }
}
// Iniciar setInterval
const intervalId = setInterval(cargarDatos, 1000); // Ejecuta cada 2 segundos

