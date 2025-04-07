document.addEventListener("DOMContentLoaded", function () {
    const startBtn = document.getElementById("start-btn");
    const endBtn = document.getElementById("end-btn");
    const cancelBtn = document.getElementById("cancel-btn");
    const tempoDecorridoEl = document.getElementById("tempo-decorrido");

    const modal = document.getElementById("modal-resumo");
    const resumoEntrada = document.getElementById("resumo-entrada");
    const resumoSaida = document.getElementById("resumo-saida");
    const resumoCarga = document.getElementById("resumo-carga");
    const descricaoInput = document.getElementById("descricao-input");
    const anotacaoInput = document.getElementById("anotacao-input");
    const fecharModal = document.getElementById("fechar-modal");
    const confirmarFinalizar = document.getElementById("confirmar-finalizar");

    let entradaTimestamp = localStorage.getItem("entradaTimestamp");
    let interval;

    function formatarTempo(segundos) {
        const horas = Math.floor(segundos / 3600).toString().padStart(2, '0');
        const minutos = Math.floor((segundos % 3600) / 60).toString().padStart(2, '0');
        const segundosRestantes = (segundos % 60).toString().padStart(2, '0');
        return `${horas}:${minutos}:${segundosRestantes}`;
    }

    function atualizarTimer() {
        if (!entradaTimestamp) {
            tempoDecorridoEl.textContent = "00:00:00";
            return;
        }

        const agora = Math.floor(Date.now() / 1000);
        const segundosPassados = agora - entradaTimestamp;
        tempoDecorridoEl.textContent = formatarTempo(segundosPassados);
    }

    function iniciarTimer() {
        clearInterval(interval);
        interval = setInterval(atualizarTimer, 1000);
    }

    // Mostrar timer inicial
    if (entradaTimestamp) {
        iniciarTimer();
        startBtn.style.display = "none";
        endBtn.style.display = "inline-block";
        cancelBtn.style.display = "inline-block";
    } else {
        tempoDecorridoEl.textContent = "00:00:00";
    }

    startBtn.addEventListener("click", function () {
        fetch("/registrar_ponto/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            entradaTimestamp = Math.floor(Date.now() / 1000);
            localStorage.setItem("entradaTimestamp", entradaTimestamp);
            iniciarTimer();
            startBtn.style.display = "none";
            endBtn.style.display = "inline-block";
            cancelBtn.style.display = "inline-block";
        });
    });

    endBtn.addEventListener("click", function () {
        const agora = Math.floor(Date.now() / 1000);
        const carga = agora - entradaTimestamp;

        resumoEntrada.textContent = new Date(entradaTimestamp * 1000).toLocaleTimeString();
        resumoSaida.textContent = new Date(agora * 1000).toLocaleTimeString();
        resumoCarga.textContent = formatarTempo(carga);

        modal.style.display = "flex";
    });

    fecharModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    confirmarFinalizar.addEventListener("click", function () {
        const descricao = descricaoInput.value;
        const anotacao = anotacaoInput.value;

        fetch("/finalizar_ponto/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            },
            body: JSON.stringify({
                descricao: descricao,
                anotacao_tecnica: anotacao
            })
        })
        .then(response => response.json())
        .then(data => {
            clearInterval(interval);
            localStorage.removeItem("entradaTimestamp");
            tempoDecorridoEl.textContent = "00:00:00";
            startBtn.style.display = "inline-block";
            endBtn.style.display = "none";
            cancelBtn.style.display = "none";
            modal.style.display = "none";
        });
    });

    cancelBtn.addEventListener("click", function () {
        clearInterval(interval);
        localStorage.removeItem("entradaTimestamp");
        tempoDecorridoEl.textContent = "00:00:00";
        startBtn.style.display = "inline-block";
        endBtn.style.display = "none";
        cancelBtn.style.display = "none";
    });
});