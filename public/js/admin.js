document.addEventListener("DOMContentLoaded", async () => {
    const tbody = document.querySelector("#bookingsTable tbody");

    async function carregarAgendamentos() {
        tbody.innerHTML = ""; // limpa a tabela antes de popular
        try {
            const res = await fetch("http://127.0.0.1:8000/agendamentos");
            const agendamentos = await res.json();

            agendamentos.forEach(a => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${a.nome}</td>
                    <td>${a.telefone}</td>
                    <td>${a.servico}</td>
                    <td>${a.data}</td>
                    <td>${a.horario}</td>
                    <td>
                        <button class="edit-btn" data-id="${a.id}">Editar</button>
                        <button class="delete-btn" data-id="${a.id}">Deletar</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });

            adicionarEventos(); // adiciona listeners aos botões
        } catch (erro) {
            alert("Erro ao carregar os agendamentos: " + erro);
        }
    }

    function adicionarEventos() {
        // DELETE
        document.querySelectorAll(".delete-btn").forEach(btn => {
            btn.addEventListener("click", async () => {
                const id = btn.dataset.id;
                if (confirm("Deseja realmente deletar este agendamento?")) {
                    try {
                        const res = await fetch(`http://127.0.0.1:8000/agendamentos/${id}`, {
                            method: "DELETE"
                        });
                        const texto = await res.text();
                        alert(texto);
                        carregarAgendamentos(); // atualiza a tabela
                    } catch (erro) {
                        alert("Erro ao deletar: " + erro);
                    }
                }
            });
        });

        // PATCH (exemplo simples: alterar horário)
        document.querySelectorAll(".edit-btn").forEach(btn => {
            btn.addEventListener("click", async () => {
                const id = btn.dataset.id;
                const novoHorario = prompt("Digite o novo horário (HH:MM):");
                if (novoHorario) {
                    try {
                        const res = await fetch(`http://127.0.0.1:8000/agendamentos/${id}`, {
                            method: "PATCH",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ horario: novoHorario })
                        });
                        const texto = await res.text();
                        alert(texto);
                        carregarAgendamentos(); // atualiza a tabela
                    } catch (erro) {
                        alert("Erro ao atualizar: " + erro);
                    }
                }
            });
        });
    }

    // Carrega os agendamentos ao abrir a página
    carregarAgendamentos();
});
