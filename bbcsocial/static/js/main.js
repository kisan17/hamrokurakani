$(document).ready(function () {

    //? WORKS FOR AUTOSIZE FOR TEXT AREAS
    autosize($('textarea'));

    $('form').keydown(function (event) {
        if (event.keyCode === 10 || event.keyCode == 13 && event.ctrlKey) {
            $('#submit').click();
        }
    })

    //? WORKS FOR JSCROLL
    $('ul.pagination').hide();
    $(function () {
        $('.infinite-scroll').jscroll({
            autoTrigger: true,
            loadingHtml: '<div class="d-flex justify-content-center"><div class="spinner-border spinner-border-sm" role="status" ><span class="sr-only">Loading...</span></div></div>',
            padding: 10,
            nextSelector: '.pagination li.active + li a',
            contentSelector: 'div.infinite-scroll',
            callback: function () {
                $('ul.pagination').remove();
                $('<h3 class="mt-2 mb-2 text-center font-weight-bold">···</h3>').appendTo('.col-md-8');
            }
        });
    });
});