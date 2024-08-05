cabecera=`<header>
<nav class="navbar navbar-expand-sm">
    <div class="logo"></div>
    <div>
        <p id="nombre" class="titulo">MataroIN</p>
    </div>
    <div class="" style="margin-left: auto;">
        <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" href="/destino.html">Destinos</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/Ofertas.html">Ofertas</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/login.html">Login</a>
            </li>
            <li><select id="idiomas"></select></li>
        </ul>
    </div>

</nav>

</header>`

pie=`<footer>

<div class="row">
    <div class="col-sm-2">
        <img class="img-fluid" ; src="/static/imagenes/logoNEGATIVO.png" />
    </div>
    <div class="col-sm-4">
        <a class="btn" href="/QuienesSomos/QuienesSomos.html">Quienes Somos</a>
    </div>
    <!-- Destino 3 -->
    <div class="col-sm-4">
        <a href="https://www.instagram.com/" target="_blank" class="btnX">
            <i class="fab fa-instagram"></i>
        </a>

        <a href="https://www.facebook.com/" target="_blank" class="btnX">
            <i class="fab fa-facebook-f"></i>
        </a>

        <a href="https://twitter.com/" target="_blank" class="btnX">
            <i class="fab fa-twitter"></i>
        </a>

    </div>
    <div class="col-sm-12">

        <p style="text-align: center;">Copyright 2024</p>
    </div>
</div>
</footer>`;

document.getElementById("headerJS").innerHTML=cabecera;
document.getElementById("footerJS").innerHTML=pie;