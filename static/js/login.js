
function validarClaves(usern, passw) {

    if (validar(usern, "usuario") && validar(passw, "password")) { location.href = "logar.html?username=" + usern + "&password=" + passw; }
    else {
        return false;
    }
}
function validar(username, cadena) {
    // Verificar si el nombre de usuario contiene espacios en blanco
    if (/\s/.test(username)) {
        alert("Error: El nombre de " + cadena + " no debe contener espacios en blanco.");
        return false;
    }

    // Verificar si el nombre de usuario tiene más de 4 caracteres
    if (username.length <= 4) {
        alert("Error: El nombre de " + cadena + " debe tener más de 4 caracteres.");
        return false;

    }

    // Si todas las validaciones pasan∫
    return true;
}
async function cargado() {
    if (cargadosDatos == true) {
        cargoV(username, password);
        clearInterval();
    };
}
function cargoV(usuario, contrasenya) {
    clientes = buscarUsuarioPassword(usuario, contrasenya, Clientes.cliente, 'clientes');
    proveedores = buscarUsuarioPassword(usuario, contrasenya, Proveedores.proveedor, 'proveedores');
    if (clientes == 'ok') {
        location.href = "clientes.html";
    }
    else if (proveedores == 'ok') {
        location.href = "proveedores.html";
    }
    else {

        location.href = "login.html";
        alert("El usuario no existe");
    }

}
function buscarUsuarioPassword(usuario, contrasenya, origen, tipo) {
    var encontrado = 'ko';
    origen.forEach((elemento) => {
        if (elemento.usuario == usuario && elemento.password == contrasenya) {
            setCookie("username", usuario, 7);
            setCookie("tipo", tipo, 7);
            encontrado = 'ok';
            return;

        }
    });
    return encontrado;
}
