document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // evita recarregar a página

        const agendamento = {
            nome: document.getElementById("name").value,
            telefone: document.getElementById("phone").value,
            servico: document.getElementById("service").value,
            data: document.getElementById("date").value,
            horario: document.getElementById("time").value,
        };

        try {
            const res = await fetch("http://127.0.0.1:8000/agendamentos", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(agendamento),
            });

            const texto = await res.text();
            alert(texto); // mostra a mensagem do servidor
            form.reset(); // limpa o formulário
        } catch (erro) {
            alert("Erro ao enviar o agendamento: " + erro);
        }
    });
});
