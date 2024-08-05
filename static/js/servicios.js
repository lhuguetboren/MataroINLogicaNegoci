function mostrarMensaje(mensaje) {
  let numb = servicios.get(mensaje);
  var mensajeDiv = document.getElementById("mensaje");
  mensajeDiv.innerHTML = numb;
  mensajeDiv.style.display = "block";
  mensajeDiv.style.color = "black";

}
function ocultarMensaje() {
  var mensajeDiv = document.getElementById("mensaje");
  mensajeDiv.style.display = "none";
}
function numeroAleatorio(max) {
  return Math.floor(Math.random() * max);
}
// Función para cambiar la imagen cuando se carga la página
function imagenCambiante(){
  var imagen = document.getElementById("presentacion");
  let source='';
  let indice=0;
  let totalFotos=Biblioteca.fotos.foto.length;

  indice = numeroAleatorio(totalFotos);
  const ahora = new Date();
  const hora = ahora.getHours();
  


  source = 'linear-gradient(rgba(0, 0, 0,' + mapearHoras(hora)+'), rgba(0, 0, 0,' + mapearHoras(hora)+')), url('+encodeURI('/static/'+Biblioteca.fotos.foto[indice].filename) + ')';

  imagen.style.backgroundImage = source;
  imagen.style.backgroundRepeat='no-repeat';
  imagen.style.backgroundSize='cover';
  imagen.style.backgroundPosition='center';

};
function mapearHoras(horas) {
  // Asegurarse de que las horas estén dentro del rango de 0 a 23
  horas = Math.max(0, Math.min(23, horas));

    // Mapear el rango de 0 a 23 al rango de 0 a 0.4
    var correspondencia = horas / 57.5; // 23/57.5 = 0.4

  // Formatear el valor como valor.valor
  return correspondencia
}
// Función para mostrar los videos por nombre
function mostrarVideosPorNombre(nombre) {
  lecturaXML('alojamientos.xml', 'Alojamientos');
  
  var container = document.getElementById("bibliotecaVideos");
  container.innerHTML = ""; // Limpiamos el contenedor

  var videosEncontrados = false;

  let videos=Biblioteca.videos.video
  for (var i = 0; i < videos.length; i++) {
      var videoURL = videos[i].url
      var videoTitulo = videos[i].title
      var videodesc = videos[i].description

      if (videoTitulo.toLowerCase().includes(nombre.toLowerCase())) { 
          videosEncontrados = true;

          var videoContainer = document.createElement("div");
          videoContainer.className = "videoContainer";

          // Crea un elemento de video y añádelo al contenedor
          var videoElement = document.createElement("video");
          videoElement.src = videoURL;
          videoElement.controls = true;

          var tituloElement = document.createElement("p");
          tituloElement.textContent = videoTitulo;

          var descriptionElement = document.createElement("p");
          descriptionElement.textContent= videodesc;

          videoContainer.appendChild(tituloElement);
          videoContainer.appendChild(videoElement);
          videoContainer.appendChild(descriptionElement);
          container.appendChild(videoContainer);
      }
  }

  if (!videosEncontrados) {
      console.error("No se encontraron videos con el nombre especificado.");
  }

  // Mostrar el botón de siguiente si hay más de un video
 

}
// Función para buscar videos por nombre
function buscarVideos() {
var nombre = document.getElementById("busqueda").value.trim();
  mostrarVideosPorNombre(nombre);
}
//Carga de desplegables
function arrayAselect(select,opcionesSO) {
  //
  let opciones=opcionesSO.sort()
  let selectHTML = '<select>';
  selectHTML +='<option> Seleccionar </opcion>'
  opciones.forEach(opcion => {
      selectHTML += `<option value="${opcion}">${opcion}</option>`;
  });

  selectHTML += '</select>';

  document.getElementById(select).innerHTML=selectHTML;
}
function arrayAULaAccion(ulc,opciones,accion) {
  let selectHTML = '<ul>';
  //console.log(opciones);
  opciones.forEach(opcion => {
      selectHTML +=`<li style='cursor:pointer;' onclick="`+accion+`('${opcion.trim()}');">${opcion}</li>`;
  });

  selectHTML += '</ul>';

  document.getElementById(ulc).innerHTML=selectHTML;
}
function ifsrc(pueblo)
{
  document.getElementById("wikipedia").src="https://es.wikipedia.org/wiki/"+pueblo
}