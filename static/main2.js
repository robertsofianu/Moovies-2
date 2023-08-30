

$(document).on('click', 'a', function () {

    const id_user = this.id;
    console.log(id_user);

    $.ajax({
        method: 'POST',
        url: '/save',
        contentType: 'application/json', 
        data: JSON.stringify({ id_user: id_user }),
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
});