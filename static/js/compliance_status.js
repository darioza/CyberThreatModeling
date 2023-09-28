    // Função para verificar todos os checkboxes
    function checkComplianceStatus() {
        // Seleciona todos os checkboxes
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:not(#compliance_projeto)');
        
        // Verifica se todos os checkboxes estão marcados
        let allChecked = true;
        checkboxes.forEach(checkbox => {
            if (!checkbox.checked) {
                allChecked = false;
            }
        });

        // Atualiza o status de compliance_projeto e compliance_projeto_hidden
        document.getElementById('compliance_projeto').checked = allChecked;
        document.getElementById('compliance_projeto_hidden').value = allChecked ? "true" : "false";
    }

    // Adiciona um evento de 'change' a todos os checkboxes para chamar a função checkComplianceStatus quando qualquer checkbox for alterado
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:not(#compliance_projeto)');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', checkComplianceStatus);
    });

    // Chama a função checkComplianceStatus inicialmente para definir o status correto
    checkComplianceStatus();