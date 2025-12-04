// ============================================================================
// FUNCIONES AUXILIARES Y UTILIDADES
// ============================================================================

function obtener(id) {  
  return document.getElementById(id);//obtiene un elemento del HTML
}

function crear(tipoElemento) {  
  return document.createElement(tipoElemento);//crea archivos HTML desde Java
}

function agregar(contenedor, elemento) {  
  return contenedor.appendChild(elemento);//añade un elemento dentro de otro en la pagina
}

function remover(elemento) {  
  return elemento.remove();//eliminar un elemento de la pagina
}

function guardarSesion(clave, valor) {  
  return sessionStorage.setItem(clave, JSON.stringify(valor));//convierte objeto js a json,guarda informacion en el navegador
}

function leerSesion(clave) {  
  let dato = sessionStorage.getItem(clave);  //busca info guardada en navegador
  return dato ? JSON.parse(dato) : null;//de json a objeto js
}

function borrarSesion(clave) {  
  return sessionStorage.removeItem(clave);
}

function mensaje(texto, tipo) {  
  let m = crear("div");  
  m.textContent = texto; //pone mensaje dentro de div
  m.className = "mensaje " + tipo; //asigna css
  agregar(document.body, m);
  setTimeout(function() { remover(m); }, 3000); 
}

async function servidor(ruta, metodo, datos) {  
  let config = {  
    method: metodo,
    headers: { "Content-Type": "application/json" }//datos van en formato JSON
  };  
  if (datos) config.body = JSON.stringify(datos);
  
  let res = await fetch(API + ruta, config);//busca y espera respuesta
  let json = await res.json();//JSON a js
  if (!res.ok) throw json; 
  return json; 
}