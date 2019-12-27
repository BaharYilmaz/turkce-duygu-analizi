


$(function() {
    $('#formYorumCek').click(function() {
 
        $.ajax({
            url: '/scraping',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
