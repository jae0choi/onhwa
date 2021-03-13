function add_song(video_id){
    edit_playlist(video_id, 'add');
}
function remove_song(video_id){
    edit_playlist(video_id, 'remove');
}
function edit_playlist(video_id, mode) {
    console.log(video_id);
    $.post('/edit_playlist', {
        video_id: video_id,
        mode : mode
    }).done(function(response) {
        console.log('added');
        
    }).fail(function(){
        console.log('failed');
    });
    load_playlist();
}
function load_playlist(){
    $.get('/load_playlist', function(playlist){
        $('#playlist').html('')
        console.log(playlist);
        $.each(playlist.data, function(index, value){
            console.log(index, value);
            $('#playlist').append("<iframe id='ytplayer' type='text/html', width='120' height='60' src='http://www.youtube.com/embed/" + value + "' frameborder='0'></iframe>");
            $('#playlist').append("<button type='button' onclick='remove_song(\"" + value +"\")'>Remove</button>");
        });
    });
}
function export_playlist(){
    $.get('/export_playlist', function(){
        console.log('export playlist');
    });

}
$(document).ready(function(){
    load_playlist()
    $('form').submit(function(event){
        event.preventDefault();
                        
        var dest_elem = $('#search_result');
        $(dest_elem).text('loading...');
        $.post('/search_youtube', {
            query: $('#query').val()
        }).done(function(response) {
            $(dest_elem).html('');
            console.log(response.data)
            $.each(response.data, function(index, value){
                $(dest_elem).append("<p>"+value['title']+"</p>");
                $(dest_elem).append("<iframe id='ytplayer' type='text/html', width='320' height='180' src='http://www.youtube.com/embed/" + value['id'] + "' frameborder='0'></iframe>");
                $(dest_elem).append("<button type='button' onclick='add_song(\"" + value['id'] +"\")'>Add to playlist</button>");
            });
        }).fail(function() {
            $(dest_elem).text("Error: Could not contact server");
        });
    });
    
});
