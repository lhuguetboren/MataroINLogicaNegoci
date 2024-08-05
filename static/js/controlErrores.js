// Función para verificar el formato del array tipo Map
function verificarFormatoServicios(servicios) {
    // Verificar si es un objeto Map
    if (!(servicios instanceof Map)) {
      throw new Error("El parámetro servicios debe ser un objeto Map.");
    }

    // Verificar si tiene al menos un elemento
    if (servicios.size === 0) {
      throw new Error("El objeto Map de servicios está vacío.");
    }

    // Verificar si cada elemento es un array de tres elementos (clave, valor, imagenURL)
    for (let servicio of servicios) {
      if (!Array.isArray(servicio) || servicio.length !== 1) {
        throw new Error("Cada elemento del objeto Map de servicios debe ser un array con tres elementos (clave, valor, imagenURL).");
      }
    }

    console.log("El objeto Map de servicios tiene el formato correcto.");
  }

  // Función para verificar la existencia de los archivos de imagen
  function verificarImagenes(servicios) {
    // Array para almacenar las promesas de carga de imágenes
    let promesas = [];

    // Iterar sobre cada elemento del mapa de servicios
    servicios.forEach(servicio => {
      // Obtener la URL de la imagen del tercer campo del array
      console.log(servicio[0]);
      let imagenURL = servicio[2];
      // Crear una nueva promesa para cargar la imagen
      let promesa = fetch(imagenURL)
        .then(response => {
          // Verificar si la respuesta es exitosa (código de estado 200)
          if (!response.ok) {
            throw new Error(`No se pudo cargar la imagen ${imagenURL}.`);
          }
        })
        .catch(error => {
          // Manejar cualquier error durante la carga de la imagen
          console.error(error.message);
        });
      // Agregar la promesa al array de promesas
      promesas.push(promesa);
    });

    // Devolver una nueva promesa que se resolverá cuando todas las promesas estén completas
    return Promise.all(promesas);
  }

  // Llamar a la función para verificar el formato de servicios
  try {
    verificarFormatoServicios(servicios);
    verificarFormatoServicios(serviciosIMG);
  } catch (error) {
    console.error("Error en el formato del objeto Map de servicios:", error.message);
  }

  // Llamar a la función para verificar la existencia de los archivos de imagen
  console.log(servicios);
  verificarImagenes(servicios)
    .then(() => {
      console.log("Todas las imágenes se cargaron exitosamente.");
      // Aquí puedes continuar con tu lógica de negocio
    })
    .catch(error => {
      console.error("Error al cargar las imágenes:", error);
      // Aquí puedes manejar cualquier error de carga de imágenes
    });

    function control() {
      var urlXML = "biblioteca.xml";
   
      // Verificar la existencia del XML
      cargarXML(urlXML, function(xml, error) {
          if (error) {
              console.error("Error al cargar el XML:", error.message);
              return;
          }
   
          // Verificar la existencia de videos
          if (!xml || xml.getElementsByTagName("video").length === 0) {
              console.error("No se encontraron videos en el archivo XML.");
              return;
          }
          
   
          // Si llegamos aquí, significa que el XML se cargó correctamente y contiene al menos un video
          console.log("El XML se cargó correctamente y contiene al menos un video.");
      });
  }