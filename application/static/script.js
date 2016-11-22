$(document).ready(function(){
    $('#AddButton').append(`
        <a href="` + window.location.pathname + `/add" class="btn btn-success btn-md" role="button">Add new</a>
        <br>
        <br>    
    `);

    $('tr').not('thead tr').hover(function(){
        var id=$(this).find('td:first').html();
        edit_path = window.location.pathname + "/edit/" + id
        delete_path = window.location.pathname + "/delete/" + id
        $(this).append( `<div class="btn-group btn-group"> \
                        <a href="` + edit_path + `" class="btn btn-warning">Edit</a> \
                        <a href="` + delete_path + `" class="btn btn-danger">Delete</a> \
                                </div>`);
        }, function(){
        $(this).children("div").remove();

        
    });
});
