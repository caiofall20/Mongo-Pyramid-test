function thumb(id, x) {
    var y = 0;
    if (x) {
        y = 1;
    }
    $.ajax({
        url: `/`,
        type: "POST",
        data: {'id': id, 'thumb': y},
        success: function(){
            location.reload(true)
        }
    })
}
