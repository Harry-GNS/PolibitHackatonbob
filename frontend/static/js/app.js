/* Frontend JS para OptiCode QA - app.js
   Mueve la lógica del dashboard a un archivo estático reutilizable.
*/
let chartTiempo = null;
let chartMemoria = null;
let metricsData = {};
let alertasActuales = [];

document.addEventListener('DOMContentLoaded', () => {
    listarAnalisisBob();
    cargarCodigos();
    log('🚀 Sistema OptiCode QA iniciado', 'success');
});

function log(mensaje, tipo = 'info') {
    const consola = document.getElementById('logConsole');
    const timestamp = new Date().toLocaleTimeString('es-ES');
    const html = `<div class="log-line log-${tipo}"><span class="log-timestamp">[${timestamp}]</span> ${mensaje}</div>`;
    consola.insertAdjacentHTML('beforeend', html);
    consola.scrollTop = consola.scrollHeight;
}

async function listarAnalisisBob() {
    try {
        const response = await fetch('/api/bob-sessions');
        const data = await response.json();

        const select = document.getElementById('bobAnalysisSelect');
        select.innerHTML = '<option value="">Seleccionar...</option>';

        if (data.success && data.archivos) {
            data.archivos.forEach(archivo => {
                const option = document.createElement('option');
                option.value = archivo.nombre;
                option.textContent = archivo.nombre.replace('.md', '');
                select.appendChild(option);
            });
            log(`✅ Cargados ${data.total} análisis desde output/informesbob/`, 'success');
        } else {
            log('ℹ️ Sin análisis en output/informesbob/ disponibles', 'warning');
        }
    } catch (error) {
        log(`❌ Error: ${error.message}`, 'error');
    }
}

function cargarAnalisisBob() {
    const nombre = document.getElementById('bobAnalysisSelect').value;
    if (!nombre) return;

    fetch(`/api/bob-sessions/${nombre}`)
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                log(`✅ Análisis de Bob cargado: ${nombre}`, 'success');
            }
        });
}

async function cargarCodigos() {
    try {
        const response = await fetch('/api/codigos');
        const data = await response.json();

        const select = document.getElementById('codigoSelect');
        select.innerHTML = '<option value="">Seleccionar...</option>';

        if (data.success && data.archivos) {
            data.archivos.forEach(archivo => {
                const option = document.createElement('option');
                option.value = archivo.nombre;
                option.textContent = archivo.nombre;
                select.appendChild(option);
            });
            log(`✅ Cargados ${data.total} códigos disponibles`, 'success');
        }
    } catch (error) {
        log(`❌ Error: ${error.message}`, 'error');
    }
}

async function ejecutarTodo() {
    const btn = document.getElementById('ejecutarBtn');
    const badge = document.getElementById('statusBadge');

    if (!document.getElementById('bobAnalysisSelect').value) {
        log('❌ Selecciona un análisis de Bob primero', 'error');
        return;
    }

    btn.disabled = true;
    badge.textContent = 'Ejecutando...';
    badge.className = 'status-badge running';

    log('⚡ Iniciando flujo completo...', 'info');

    try {
        const bobFile = document.getElementById('bobAnalysisSelect').value;
        const codigo = document.getElementById('codigoSelect').value || '';

        const response = await fetch('/api/ejecutar-todo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ bob_analysis_file: bobFile, codigo })
        });
        const data = await response.json();

        if (data.success) {
            metricsData = data.metricas;
            alertasActuales = data.alertas || [];

            actualizarGraficos();
            actualizarTabla();
            actualizarAlertas();

            log('✅ Flujo completo ejecutado exitosamente', 'success');
            badge.textContent = 'Proceso Completado ✓';
            badge.className = 'status-badge';

            if (data.archivo_reporte) {
                const archivo = data.archivo_reporte.split(/[/\\]/).pop();
                if (archivo) {
                    window.open(`/api/reportes/${encodeURIComponent(archivo)}`, '_blank');
                }
            }
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        log(`❌ Error: ${error.message}`, 'error');
        badge.textContent = 'Error';
    } finally {
        btn.disabled = false;
    }
}

function actualizarGraficos() {
    const sizes = Object.keys(metricsData).sort((a, b) => parseInt(a) - parseInt(b));
    const tiempos = sizes.map(s => metricsData[s].time_ms);
    const memorias = sizes.map(s => metricsData[s].memory_mb);

    const ctxTiempo = document.getElementById('chartTiempo').getContext('2d');
    if (chartTiempo) chartTiempo.destroy();

    chartTiempo = new Chart(ctxTiempo, {
        type: 'line',
        data: {
            labels: sizes.map(s => `N=${s}`),
            datasets: [{
                label: 'Tiempo (ms)',
                data: tiempos,
                borderColor: '#0F62FE',
                backgroundColor: 'rgba(15, 98, 254, 0.1)',
                fill: true,
                tension: 0.3,
                pointBackgroundColor: '#0F62FE',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true }, x: { grid: { display: false } } }
        }
    });

    const ctxMemoria = document.getElementById('chartMemoria').getContext('2d');
    if (chartMemoria) chartMemoria.destroy();

    chartMemoria = new Chart(ctxMemoria, {
        type: 'bar',
        data: {
            labels: sizes.map(s => `N=${s}`),
            datasets: [{ label: 'Memoria (MB)', data: memorias, backgroundColor: '#24A148', borderRadius: 4 }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true }, x: { grid: { display: false } } }
        }
    });
}

function actualizarTabla() {
    const tbody = document.getElementById('metricsTableBody');
    tbody.innerHTML = '';

    const sizes = Object.keys(metricsData).sort((a, b) => parseInt(a) - parseInt(b));

    sizes.forEach(size => {
        const m = metricsData[size];
        const desv = m.samples_time.length > 1
            ? Math.sqrt(m.samples_time.reduce((sum, val) => sum + Math.pow(val - m.time_ms, 2), 0) / m.samples_time.length)
            : 0;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>N = ${size}</strong></td>
            <td class="${m.time_ms > 1000 ? 'value-error' : (m.time_ms > 100 ? 'value-warning' : 'value-good')}">${m.time_ms.toFixed(2)}</td>
            <td class="${m.memory_mb > 100 ? 'value-warning' : 'value-good'}">${m.memory_mb.toFixed(2)}</td>
            <td>${desv.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });

    document.getElementById('alertasCount').textContent = alertasActuales.length;
}

function actualizarAlertas() {
    const container = document.getElementById('alertasContainer');

    if (!alertasActuales || alertasActuales.length === 0) {
        container.innerHTML = '<div class="empty-state" style="padding: 0.8rem;">✓ Sin alertas</div>';
        return;
    }

    container.innerHTML = '';
    alertasActuales.forEach(alerta => {
        const div = document.createElement('div');
        div.className = `alert ${alerta.nivel}`;
        div.innerHTML = `
            <div class="alert-icon">${alerta.icono}</div>
            <div class="alert-content">
                <div class="alert-title">${alerta.tipo}</div>
                <div class="alert-message">${alerta.mensaje}</div>
            </div>
        `;
        container.appendChild(div);
    });
}
