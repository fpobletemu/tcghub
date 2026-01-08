// Variables globales
let torneosTodos = [];
let ubicacionesDisponibles = new Set();

// Cargar torneos al abrir la página
document.addEventListener('DOMContentLoaded', async () => {
    await cargarTorneos();
});

// Inicializar con datos dummy si es necesario
async function inicializarDummy() {
    try {
        const response = await fetch('/api/init-dummy', { method: 'POST' });
        if (response.status === 201) {
            console.log('Torneos dummy creados');
        }
    } catch (error) {
        console.error('Error al inicializar dummy:', error);
    }
}

// Cargar todos los torneos
async function cargarTorneos() {
    try {
        const response = await fetch('/api/torneos');
        torneosTodos = await response.json();
        ubicacionesDisponibles = new Set(torneosTodos.map(t => t.ubicacion).filter(u => u));
        actualizarSelectUbicaciones();
        await renderizarTorneos();
    } catch (error) {
        console.error('Error al cargar torneos:', error);
    }
}

// Renderizar torneos en la grid (usando HTMX)
async function renderizarTorneos() {
    try {
        const response = await fetch('/api/filtrar?filtro-fecha=&filtro-ubicacion=&filtro-juego=');
        const html = await response.text();
        document.getElementById('grid-torneos').innerHTML = html;
    } catch (error) {
        console.error('Error al renderizar torneos:', error);
    }
}

// Actualizar opciones del select de ubicaciones
function actualizarSelectUbicaciones() {
    const select = document.getElementById('filtro-ubicacion');
    const ubicacionesArray = Array.from(ubicacionesDisponibles).sort();
    
    const opcionesActuales = Array.from(select.querySelectorAll('option')).slice(1);
    opcionesActuales.forEach(opt => opt.remove());
    
    ubicacionesArray.forEach(ubicacion => {
        const option = document.createElement('option');
        option.value = ubicacion;
        option.textContent = ubicacion;
        select.appendChild(option);
    });
}

// Aplicar filtros
function aplicarFiltros() {
    const fechaFiltro = document.getElementById('filtro-fecha').value;
    const ubicacionFiltro = document.getElementById('filtro-ubicacion').value;
    
    let torneosFiltrados = torneosTodos;
    
    // Filtrar por fecha
    if (fechaFiltro) {
        torneosFiltrados = torneosFiltrados.filter(t => t.fecha === fechaFiltro);
    }
    
    // Filtrar por ubicación
    if (ubicacionFiltro) {
        torneosFiltrados = torneosFiltrados.filter(t => t.ubicacion === ubicacionFiltro);
    }
    
    mostrarTorneos(torneosFiltrados);
}

// Mostrar torneos en la grid
function mostrarTorneos(torneos) {
    const grid = document.getElementById('grid-torneos');
    
    if (torneos.length === 0) {
        grid.innerHTML = '<p class="mensaje-carga sin-resultados">No hay torneos que coincidan con los filtros</p>';
        return;
    }
    
    grid.innerHTML = torneos.map(torneo => crearTarjeta(torneo)).join('');
}

// Crear HTML de tarjeta
function crearTarjeta(torneo) {
    const fechaFormato = new Date(torneo.fecha).toLocaleDateString('es-ES', { 
        weekday: 'short', 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
    
    return `
        <div class="tarjeta-torneo">
            <div class="tarjeta-header">
                <h3 class="tarjeta-titulo">${torneo.nombre_tienda}</h3>
            </div>
            
            <div class="tarjeta-badges">
                <span class="badge-juego">${torneo.tipo_juego}</span>
                <span class="badge-categoria">${torneo.categoria}</span>
                <span class="badge-tipo">${torneo.tipo_torneo}</span>
            </div>
            
            <div class="tarjeta-info">
                <div class="info-item">
                    <div class="info-label">Fecha</div>
                    <div class="info-value">${fechaFormato}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Hora</div>
                    <div class="info-value">${torneo.hora}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Ubicación</div>
                    <div class="info-value">${torneo.ubicacion || 'No especificada'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Premio</div>
                    <div class="info-value">${torneo.premio || 'No especificado'}</div>
                </div>
            </div>
            
            <div class="tarjeta-acciones">
                <button class="btn-editar" onclick="abrirFormulario(${torneo.id})">Editar</button>
                <button class="btn-eliminar" onclick="eliminarTorneo(${torneo.id})">Eliminar</button>
            </div>
        </div>
    `;
}

// Abrir formulario para crear/editar
async function abrirFormulario(id = null) {
    const modal = document.getElementById('modal');
    const form = document.getElementById('formulario-torneo');
    const tituloModal = document.getElementById('titulo-modal');
    
    form.reset();
    document.getElementById('torneo-id').value = '';
    
    if (id) {
        tituloModal.textContent = 'Editar Torneo';
        const torneo = torneosTodos.find(t => t.id === id);
        
        if (torneo) {
            document.getElementById('torneo-id').value = torneo.id;
            document.getElementById('nombre_tienda').value = torneo.nombre_tienda;
            document.getElementById('ubicacion').value = torneo.ubicacion;
            document.getElementById('hora').value = torneo.hora;
            document.getElementById('fecha').value = torneo.fecha;
            document.getElementById('premio').value = torneo.premio;
            document.getElementById('tipo_juego').value = torneo.tipo_juego;
            document.getElementById('categoria').value = torneo.categoria;
            document.getElementById('tipo_torneo').value = torneo.tipo_torneo;
            document.getElementById('imagen').value = torneo.imagen || '';
        }
    } else {
        tituloModal.textContent = 'Crear Nuevo Torneo';
    }
    
    modal.classList.remove('hidden');
}

// Cerrar formulario
function cerrarFormulario(event) {
    if (event && event.target.id !== 'modal') return;
    
    const modal = document.getElementById('modal');
    modal.classList.add('hidden');
    document.getElementById('formulario-torneo').reset();
    document.getElementById('torneo-id').value = '';
}

// Guardar torneo (crear o actualizar)
async function guardarTorneo() {
    const id = document.getElementById('torneo-id').value;
    const datos = {
        nombre_tienda: document.getElementById('nombre_tienda').value,
        ubicacion: document.getElementById('ubicacion').value,
        hora: document.getElementById('hora').value,
        fecha: document.getElementById('fecha').value,
        premio: document.getElementById('premio').value,
        tipo_juego: document.getElementById('tipo_juego').value,
        categoria: document.getElementById('categoria').value,
        tipo_torneo: document.getElementById('tipo_torneo').value,
        imagen: document.getElementById('imagen').value
    };
    
    try {
        const url = id ? `/api/torneos/${id}` : '/api/torneos';
        const metodo = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: metodo,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });
        
        if (response.ok) {
            cerrarFormulario();
            await cargarTorneos();
            mostrarNotificacion(id ? 'Torneo actualizado' : 'Torneo creado', 'exito');
        } else if (response.status === 401) {
            alert('Debes iniciar sesión para realizar esta acción');
            window.location.href = '/admin';
        } else {
            mostrarNotificacion('Error al guardar el torneo', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion('Error al guardar el torneo', 'error');
    }
}

// Eliminar torneo
async function eliminarTorneo(id) {
    // Si no se pasa ID, usar el del formulario actual
    if (!id) {
        id = document.getElementById('torneo-id').value;
    }
    
    if (!id) {
        alert('No hay torneo seleccionado');
        return;
    }
    
    try {
        const response = await fetch(`/api/torneos/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            cerrarFormulario();
            await cargarTorneos();
            mostrarNotificacion('Torneo eliminado', 'exito');
        } else if (response.status === 401) {
            alert('Debes iniciar sesión para eliminar torneos');
            window.location.href = '/admin';
        } else {
            mostrarNotificacion('Error al eliminar el torneo', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion('Error al eliminar el torneo', 'error');
    }
}

// Limpiar filtro de fecha
function limpiarFiltroFecha() {
    document.getElementById('filtro-fecha').value = '';
    htmx.ajax('GET', '/api/filtrar?filtro-fecha=&filtro-ubicacion=' + document.getElementById('filtro-ubicacion').value + '&filtro-juego=' + document.getElementById('filtro-juego').value, '#grid-torneos');
}

// Limpiar todos los filtros
function limpiarFiltros() {
    document.getElementById('filtro-fecha').value = '';
    document.getElementById('filtro-ubicacion').value = '';
    document.getElementById('filtro-juego').value = '';
    htmx.ajax('GET', '/api/filtrar?filtro-fecha=&filtro-ubicacion=&filtro-juego=', '#grid-torneos');
}

// Mostrar notificación simple
function mostrarNotificacion(mensaje, tipo) {
    console.log(`[${tipo.toUpperCase()}] ${mensaje}`);
}

// Manejar envío del formulario
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('formulario-torneo').addEventListener('submit', async (e) => {
        e.preventDefault();
        await guardarTorneo();
    });
});
