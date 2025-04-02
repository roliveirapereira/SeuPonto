document.addEventListener("DOMContentLoaded", function () {
    let timer;
    let elapsedSeconds = 0;
    let isPaused = false;

    const timerDisplay = document.getElementById("timer");
    const iniciarBtn = document.getElementById("start-btn");
    const pauseBtn = document.getElementById("pause-btn");
    const resumeBtn = document.getElementById("resume-btn");
    const stopBtn = document.getElementById("stop-btn");
    const cancelBtn = document.getElementById("cancel-btn"); // Novo botão de cancelar

    // Antes de iniciar, esconde todos os botões, exceto "Iniciar ponto"
    pauseBtn.style.display = "none";
    resumeBtn.style.display = "none";
    stopBtn.style.display = "none";
    cancelBtn.style.display = "none";

    function startTimer() {
        timer = setInterval(() => {
            if (!isPaused) {
                elapsedSeconds++;
                updateTimerDisplay();
            }
        }, 1000);
    }

    function updateTimerDisplay() {
        let hours = Math.floor(elapsedSeconds / 3600).toString().padStart(2, "0");
        let minutes = Math.floor((elapsedSeconds % 3600) / 60).toString().padStart(2, "0");
        let seconds = (elapsedSeconds % 60).toString().padStart(2, "0");
        timerDisplay.innerText = `${hours}:${minutes}:${seconds}`;
    }

    iniciarBtn.addEventListener("click", function () {
        iniciarBtn.style.display = "none"; // Esconder botão de iniciar
        pauseBtn.style.display = "inline-block";
        stopBtn.style.display = "inline-block";
        cancelBtn.style.display = "inline-block"; // Mostrar o botão de cancelar

        startTimer();
        fetch("/registrar_ponto/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "action=iniciar",
        });
    });

    pauseBtn.addEventListener("click", function () {
        isPaused = true;
        pauseBtn.style.display = "none";
        resumeBtn.style.display = "inline-block";

        fetch("/registrar_ponto/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "action=pausar",
        });
    });

    resumeBtn.addEventListener("click", function () {
        isPaused = false;
        resumeBtn.style.display = "none";
        pauseBtn.style.display = "inline-block";

        fetch("/registrar_ponto/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "action=continuar",
        });
    });

    stopBtn.addEventListener("click", function () {
        clearInterval(timer);
        stopBtn.style.display = "none";
        pauseBtn.style.display = "none";
        resumeBtn.style.display = "none";
        cancelBtn.style.display = "none";
        timerDisplay.innerText = "Finalizado";

        fetch("/registrar_ponto/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "action=finalizar",
        });
    });

    cancelBtn.addEventListener("click", function () {
        clearInterval(timer);
        elapsedSeconds = 0;
        timerDisplay.innerText = "00:00:00";

        // Esconde todos os botões e mostra só o de iniciar
        pauseBtn.style.display = "none";
        resumeBtn.style.display = "none";
        stopBtn.style.display = "none";
        cancelBtn.style.display = "none";
        iniciarBtn.style.display = "inline-block";

        // Chamada para excluir o ponto iniciado
        fetch("/registrar_ponto/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "action=cancelar",
        });
    });

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});

