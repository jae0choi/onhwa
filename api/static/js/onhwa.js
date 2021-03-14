function add_song(video_id, video_title){
    edit_playlist(video_id, video_title, 'add');
}
function remove_song(video_id){
    edit_playlist(video_id, '', 'remove');
}
function edit_playlist(video_id, video_title, mode) {
    console.log(video_id);
    $.post('/edit_playlist', {
        video_id: video_id,
        video_title: video_title,
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
            $('#playlist').append("<li class='added-song'><img class='thumbnail' src='http://img.youtube.com/vi/" + value['video_id'] + "/default.jpg'><p class='title'>"+value['video_title']+"</p><button class='remove' type='button' onclick='remove_song(\"" + value['video_id'] +"\")'>Remove</button></li>");

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
    $( "#playlist" ).sortable();
    $( "#playlist" ).disableSelection();

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
                $(dest_elem).append("<div class='searched-song'><iframe id='ytplayer' class='player-thumbnail' type='text/html', width='320' height='180' src='http://www.youtube.com/embed/" + value['video_id'] + "' frameborder='0'></iframe><p>"+value['video_title']+"</p><button type='button' onclick='add_song(\"" + value['video_id'] +"\", \"" + value['video_title'] + "\")'>Add to playlist</button></div>");
            });
        }).fail(function() {
            $(dest_elem).text("Error: Could not contact server");
        });
    });
    
});
