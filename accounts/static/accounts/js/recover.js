function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

// console.log(getParameterByName('token'))

var sendPasswordChange = function(){
    var data = {
        'token': getParameterByName('token'),
        'password': $('#new-password').val(),
    };

    $.ajax({
        url: 'http://cepretareas.herokuapp.com/accounts/password/reset',
        type: 'POST',
        data: data,
        dataType: "json",
        error: function(xhr, ajaxOptions, thrownError){
            console.log('Error');
            $('#msg').html("Hubo un error al cambiar las contraseñas");
        },
        success: function(resp){
            console.log(resp);
            $('#rp_form').hide();
            $('#msg').html("El cambio de contraseñas fue exitoso");
        }
    })
}

var validatePasswords = function(){
    var pass1 = $('#new-password').val();
    var pass2 = $('#confirm-new-password').val()
    $('#msg').html("");
    if(pass1 === pass2){
        sendPasswordChange();
    }else{
        $('#msg').html("Las contraseñas no coinciden");
    }
}

$('#btn-update-password').click(validatePasswords);
