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

function lecturaXML(url, nombre) {
    fetch('/static/xml/' + url)
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(data, "text/xml");
            const objeto = xmlToObj(xmlDoc.documentElement);

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
            
            archiv++;
            if (archiv >= archivos.length) {
                cargadosDatos = true;
                clearInterval(intervalId);  // Detenemos el intervalo cuando todos los archivos están cargados
                main();  // Llamamos a la función principal
            }
        })
        .catch(error => console.error('Error al obtener el archivo XML:', error));
}

async function cargarDatos() {
    if (!cargadosDatos) {  // Solo cargamos datos si no se han cargado aún
        archivos.forEach((elemento) => {
            lecturaXML(elemento["archivo"], elemento["nombre"]);
        });
    }
}

// Iniciar setInterval para cargar datos
const intervalId = setInterval(cargarDatos, 3000);
