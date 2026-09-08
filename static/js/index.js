function abrirModal(tipoInicial) {

    const modal = document.getElementById("modal-lancamento");

    const selectTipo = document.getElementById("modal-tipo");

    modal.style.display = "flex";

    // LIMPA opções
    selectTipo.innerHTML = "";

    // =========================
    // ENTRADA
    // =========================

    if (tipoInicial === "Receita") {

        const option = document.createElement("option");

        option.value = "Receita";

        option.textContent = "Receita";

        selectTipo.appendChild(option);
    }

    // =========================
    // SAÍDA
    // =========================

    else {

        const option1 = document.createElement("option");

        option1.value = "Despesa";

        option1.textContent = "Despesa";

        selectTipo.appendChild(option1);

        const option2 = document.createElement("option");

        option2.value = "Despesa Emergencial";

        option2.textContent = "Despesa Emergencial";

        selectTipo.appendChild(option2);
    }
}

function fecharModal() {

    const modal = document.getElementById("modal-lancamento");

    modal.style.display = "none";
}