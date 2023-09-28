$(document).ready(function() {
  $('#componentes_multi').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
      var selectedCount = $(this).selectpicker('val').length;

      if (selectedCount > 0) {
          $('label[for="componentes_multi"]').addClass('text-muted');
      } else {
          $('label[for="componentes_multi"]').removeClass('text-muted');
      }
  });
});
