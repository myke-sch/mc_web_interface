const removeSuccess = () => {
  $('.button').removeClass('success');
};

$(document).ready(() => {
  $('.button').click(function() {
    $(this).addClass('success');
    setTimeout(removeSuccess, 3000);
  });
});

