document.addEventListener('DOMContentLoaded', () => {

    // Confirmação de exclusão
    const botoesExcluir = document.querySelectorAll('.btn-danger');

    botoesExcluir.forEach(botao => {

        botao.addEventListener('click', function(event){

            const confirmar = confirm(
                'Deseja realmente excluir esta movimentação?'
            );

            if(!confirmar){
                event.preventDefault();
            }

        });

    });

    // Efeito fade na tabela
    const tabela = document.querySelector('table');

    if(tabela){
        tabela.classList.add('fade-in');
    }

    function editarPerfil() {
    alert("Abrir tela de edição do perfil.");
}

function logout() {
    let confirmar = confirm("Deseja realmente sair?");

    if(confirmar){
        alert("Logout realizado!");
        
        // Exemplo:
        // window.location.href = "login.html";
    }
}

});

{% if conta_editando %}
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const modal = new bootstrap.Modal(document.getElementById('modalNovoBanco'));
            modal.show();
        });
    </script>
    {% endif %}

