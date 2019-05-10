function postUploadHandler(key, file_name) {

    var newForm = jQuery('<form>', {
        'action': '/upload_callback',
        'method':'POST',
    }).append(jQuery('<input>', {
        'name': 'key',
        'value': key,
        'type': 'hidden'
    })).append(jQuery('<input>', {
        'name': 'file_name',
        'value': file_name,
        'type': 'hidden'
    }));
    newForm.hide().appendTo("body").submit();
}


function upload(url, file, key) {
    $.ajax({
        url: url,
        type: 'PUT',
        data: file,
        contentType: file.type,
        success: function() {
            $('#messages').html('<p>Uploaded: ' + file.name + '</p>');
            postUploadHandler(key, file.name)
        },

        error: function(result) {
            $('#messages').html("Error: " + result);
        },

        beforeSend: function() {

            $('#messages').html("Uploading....")
        },
        processData: false
    });
}


var uploadCallback = function(uploadedFile) {
    return function(data) {
        var url = data['url'];
        var key = data['key'];
        upload(url, uploadedFile, key);
    }
};


function handleFiles(files) {
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var filename = file.name;
        $.getJSON("/get_signed_url", {
                filename: filename,
                content_type: file.type
            },
            uploadCallback(file)
        );
    }
}
