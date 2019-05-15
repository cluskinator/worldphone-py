function hide_flask_message_container() {
    $('#flash_message_container').slideUp('fast');
}

$(document).ready(function() {
    /* Show and hide flash message. */
    $('#flash_message_container').slideDown(function() {
        setTimeout(hide_flask_message_container, 3000);
    });
});

$('li.dropdown').on('click', function (event) {
    $(this).toggleClass("open");
    event.stopPropagation();
});

$('body').on('click', function (e) {
    if (!$('li.dropdown').is(e.target) && $('li.dropdown').has(e.target).length === 0 && $('.open').has(e.target).length === 0) {
        $('li.dropdown').removeClass('open');
    }
});

// $('li.dropdown').on('click', function (event) {
//     $(this).toggleClass("open");
//     event.stopPropagation();
// });