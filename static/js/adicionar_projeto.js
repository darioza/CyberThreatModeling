function showText(element) {
    element.textContent = "+ Adicionar Projeto";
    element.classList.remove("rounded-circle");
    element.classList.add("rounded");
    element.classList.add("expanded");  // Classe para aumentar o tamanho
}

function hideText(element) {
    element.textContent = "+";
    element.classList.remove("rounded");
    element.classList.remove("expanded");  // Remove a classe de tamanho aumentado
}
