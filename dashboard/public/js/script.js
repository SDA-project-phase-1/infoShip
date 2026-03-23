//? GLOBAL VARIABLES
let startTime = Date.now();

let hueRotation = 180;
let demoTime = 0;
let runningSum = 0;

const socket = io();
let arr_of_charts = [];
const parentContainer = document.getElementById('all-the-graphs');
const chart_config = {};
let node_sa_config_value = {};

const chartStyles = [
    // Style 0 — Hue-shifting cyan (dynamic, follows hueRotation)
    (h) => ({
        borderColor: `hsl(${h}, 80%, 60%)`,
        backgroundColor: `hsla(${h}, 80%, 60%, 0.08)`,
        pointBackgroundColor: `hsl(${h}, 80%, 60%)`,
        pointRadius: 4,
        pointHoverRadius: 7,
        fill: true,
        tension: 0.4,
        borderWidth: 2,
        shadowColor: `hsl(${h}, 80%, 60%)`,
        shadowBlur: 15,
        borderDash: [],
    }),
    // Style 1 — Pink dashed
    (h) => ({
        borderColor: 'hsl(340, 80%, 60%)',
        backgroundColor: 'hsla(340, 80%, 60%, 0.07)',
        pointBackgroundColor: 'hsl(340, 80%, 60%)',
        pointRadius: 4,
        pointHoverRadius: 7,
        fill: true,
        tension: 0.4,
        borderWidth: 2,
        shadowColor: 'hsl(340, 80%, 60%)',
        shadowBlur: 15,
        borderDash: [6, 4],
    }),
    // Style 2 — Green dotted
    (h) => ({
        borderColor: 'hsl(120, 70%, 55%)',
        backgroundColor: 'hsla(120, 70%, 55%, 0.07)',
        pointBackgroundColor: 'hsl(120, 70%, 55%)',
        pointRadius: 4,
        pointHoverRadius: 7,
        fill: true,
        tension: 0.4,
        borderWidth: 2,
        shadowColor: 'hsl(120, 70%, 55%)',
        shadowBlur: 15,
        borderDash: [2, 6],
    }),
    // Style 3 — Orange solid, no fill
    (h) => ({
        borderColor: 'hsl(30, 90%, 60%)',
        backgroundColor: 'hsla(30, 90%, 60%, 0.07)',
        pointBackgroundColor: 'hsl(30, 90%, 60%)',
        pointRadius: 4,
        pointHoverRadius: 7,
        fill: false,
        tension: 0.4,
        borderWidth: 2,
        shadowColor: 'hsl(30, 90%, 60%)',
        shadowBlur: 15,
        borderDash: [],
    }),
    // Style 4 — Purple long dash, sharp tension
    (h) => ({
        borderColor: 'hsl(270, 80%, 65%)',
        backgroundColor: 'hsla(270, 80%, 65%, 0.07)',
        pointBackgroundColor: 'hsl(270, 80%, 65%)',
        pointRadius: 5,
        pointHoverRadius: 9,
        fill: true,
        tension: 0.1,
        borderWidth: 2,
        shadowColor: 'hsl(270, 80%, 65%)',
        shadowBlur: 15,
        borderDash: [10, 4],
    }),
    // Style 5 — Red flat, thick border, no fill
    (h) => ({
        borderColor: 'hsl(0, 85%, 60%)',
        backgroundColor: 'hsla(0, 85%, 60%, 0.07)',
        pointBackgroundColor: 'hsl(0, 85%, 60%)',
        pointRadius: 6,
        pointHoverRadius: 10,
        fill: false,
        tension: 0,           // sharp/angular lines
        borderWidth: 3,
        shadowColor: 'hsl(0, 85%, 60%)',
        shadowBlur: 20,
        borderDash: [],
    }),
    // Style 6 — Yellow, tiny points, filled
    (h) => ({
        borderColor: 'hsl(55, 90%, 55%)',
        backgroundColor: 'hsla(55, 90%, 55%, 0.06)',
        pointBackgroundColor: 'hsl(55, 90%, 55%)',
        pointRadius: 2,
        pointHoverRadius: 6,
        fill: true,
        tension: 0.5,         // very smooth
        borderWidth: 2,
        shadowColor: 'hsl(55, 90%, 55%)',
        shadowBlur: 12,
        borderDash: [],
    }),
    // Style 7 — Teal, dash-dot pattern, no fill
    (h) => ({
        borderColor: 'hsl(175, 75%, 50%)',
        backgroundColor: 'hsla(175, 75%, 50%, 0.07)',
        pointBackgroundColor: 'hsl(175, 75%, 50%)',
        pointRadius: 4,
        pointHoverRadius: 8,
        fill: false,
        tension: 0.3,
        borderWidth: 2,
        shadowColor: 'hsl(175, 75%, 50%)',
        shadowBlur: 15,
        borderDash: [8, 3, 2, 3], // dash-dot-dash
    }),
];

const commonOptions = {
    responsive: true, //adjust hojaye khudi
    maintainAspectRatio: false, //style sahi nahi horaha tha iske begair
    scales: {
        y: {
            grid: { color: 'rgba(255,255,255,0.04)', drawBorder: false },
            ticks: {
                color: '#58a6ff',
                font: { family: "'Share Tech Mono', monospace", size: 13, weight: 'bold' },
                padding: 10
            },
            title: {
                display: true, text: 'VALUE',
                color: '#8b949e',
                font: { size: 11, weight: 'bold', letterSpacing: 2 }
            }
        },
        x: {
            grid: { display: false },
            ticks: {
                color: '#8b949e',
                font: { family: "'Share Tech Mono', monospace", size: 11, style: 'italic' },
                maxRotation: 45, minRotation: 45
            },
            title: {
                display: true, text: 'TIMESTAMP / PERIOD',
                color: '#8b949e',
                font: { size: 11, weight: 'bold' }
            }
        }
    },
    plugins: {
        legend: {
            display: true, position: 'top',
            labels: {
                color: '#e6edf3',
                font: { family: "'Orbitron', monospace", size: 12, weight: '700' },
                padding: 20,
                usePointStyle: true
            }
        }
    },
    animation: { duration: 300 }
};

let packetCount = 0;


//?FUNCTIONS
setInterval(() => {
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const h = String(Math.floor(elapsed / 3600)).padStart(2, '0');
    const m = String(Math.floor((elapsed % 3600) / 60)).padStart(2, '0');
    const s = String(elapsed % 60).padStart(2, '0');
    document.getElementById('uptime-counter').textContent = `${h}:${m}:${s}`;
}, 1000);


//?temp wo add kar deta aik effect and then remove it
function glitchUpdate(elId, boxId, val) {
    const el = document.getElementById(elId);
    const box = document.getElementById(boxId);
    el.textContent = val;

    const currentState = ['state-green', 'state-yellow', 'state-red']
        .find(s => el.classList.contains(s));

    el.classList.remove('glitch');
    void el.offsetWidth;
    el.classList.add('glitch');
    if (currentState) el.classList.add(currentState);

    box.classList.remove('pulse-box');
    void box.offsetWidth;
    box.classList.add('pulse-box');
}

const WARN_THRESHOLD = 50;
const CRIT_THRESHOLD = 80;
const MAX_CAPACITY = 100;
let queueMaxSize = 100;

function applyHealthState(valueId, barId, statusId, boxId, size) {
    const valueEl = document.getElementById(valueId);
    const barEl = document.getElementById(barId);
    const statusEl = document.getElementById(statusId);
    const boxEl = document.getElementById(boxId);

    const states = ['state-green', 'state-yellow', 'state-red'];
    [valueEl, barEl, statusEl, boxEl].forEach(el => el.classList.remove(...states));

    // Thresholds derived from config size
    const warn = queueMaxSize * 0.5;
    const crit = queueMaxSize * 0.8;

    let state, label;
    console.log(warn,crit,queueMaxSize);
    if (size >= crit) {
        console.log("RED");
        state = 'state-red'; label = 'BACKPRESSURE';
    }
    else if (size >= warn) {
        console.log("YELLOW");
        state = 'state-yellow'; label = 'FILLING';
    }
    else {
        console.log("GREEN");
        state = 'state-green'; label = 'NOMINAL';
    }

    [valueEl, barEl, statusEl, boxEl].forEach(el => el.classList.add(state));
    statusEl.textContent = label;
    barEl.style.width = Math.min((size / queueMaxSize) * 100, 100) + '%';
}

//? HANDLES WHEN A PACKET ARRIVES
socket.on("packet-arrived", (packet) => {
    packetCount++;
    document.getElementById('packet-count').textContent = packetCount;
    hueRotation = (hueRotation + 10) % 360;

    let j = 0;
    for (let i in node_sa_config_value) {
        const chart = arr_of_charts[j];
        const hue = (hueRotation + j * 40) % 360;

        // shift hue
        chart.data.datasets[0].borderColor = `hsl(${hue}, 80%, 60%)`;
        chart.data.datasets[0].backgroundColor = `hsla(${hue}, 80%, 60%, 0.08)`;
        chart.data.datasets[0].pointBackgroundColor = `hsl(${hue}, 80%, 60%)`;

        chart.data.labels.push(packet[chart_config[i]["x_axis"]]);
        chart.data.datasets[0].data.push(packet[chart_config[i]["y_axis"]]);


        if (chart.data.labels.length > 20) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }

        chart.update();
        j++;
    }
})

socket.on("telemetry-arrived", (data) => {
    console.log(data);
    glitchUpdate('raw-size', 'box-raw', data.raw || 0);
    glitchUpdate('int-size', 'box-int', data.int || 0);
    glitchUpdate('proc-size', 'box-proc', data.proc || 0);


    applyHealthState('raw-size', 'bar-raw', 'status-raw', 'box-raw', data.raw);
    applyHealthState('int-size', 'bar-int', 'status-int', 'box-int', data.int);
    applyHealthState('proc-size', 'bar-proc', 'status-proc', 'box-proc', data.proc);
})

socket.on("config-arrived", (config) => {
    console.log("UI Config received:", config);
    node_sa_config_value = config;

    let j = 0;
    for (let i in config) {
        const outer_div = document.createElement('div'); //
        outer_div.classList.add('chart-container'); //

        const inner_div = document.createElement('div');;
        inner_div.classList.add("card-label");
        inner_div.id = config[i]["title"] + "_label";
        inner_div.textContent = config[i]["title"];

        const canvas = document.createElement('canvas');
        canvas.id = config[i]["title"];

        outer_div.appendChild(inner_div);
        outer_div.appendChild(canvas);

        parentContainer.appendChild(outer_div);
        const styleObj = chartStyles[j % chartStyles.length](hueRotation);
        chart_config[i] = {
            "x_axis": config[i]["x_axis"],
            "y_axis": config[i]["y_axis"]
        }

        arr_of_charts[j] = new Chart(canvas, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: config[i]["title"],
                    data: [],
                    ...styleObj
                }]
            },
            options: commonOptions
        })
        j++;
    }
    console.log(chart_config);
});



socket.on("telemetry-config-arrived", (telemetry) => {
    console.log("Telemetry config received:", telemetry);
     queueMaxSize = telemetry.size;

});



