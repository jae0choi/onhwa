var video_ids;

function add_song(video_id, video_title){
    edit_playlist(video_id, video_title, 'add');
}
function remove_song(video_id){
    edit_playlist(video_id, '', 'remove');
}
function edit_playlist(video_id, video_title, mode) {
    //console.log(video_id);
    $.post('/edit_playlist', {
        video_id: video_id,
        video_title: video_title,
        mode : mode
    }).done(function(response) {
        console.log('Song edit success');
        
    }).fail(function(){
        console.log('Song edit failed');
    });
    load_playlist();
}
function load_playlist(){
    $.get('/load_playlist', function(playlist){
        $('#playlist').html('')
     //   console.log(playlist);

        video_ids = [];
        $.each(playlist.data, function(index, value){
            console.log(index, value);
            video_ids.push(value['video_id']);
            $('#playlist').append("<li class='added-song'><img class='icon play-white' src='./static/image/play-white.svg'/><img class='icon pause-white' src='./static/image/pause-white.svg'/><img class='thumbnail' src='http://img.youtube.com/vi/" + value['video_id'] + "/default.jpg'><p class='title'>"+value['video_title']+"</p><img class='icon trash' src='static/image/trash.svg' onclick='remove_song(\"" + value['video_id'] +"\")'/></li>");
        });
    });
}
function export_playlist(){
    $.get('/export_playlist', function(){
        console.log('export playlist');
    });

}
$(document).ready(function(){
    init_player();
    load_playlist();

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
         //   console.log(response.data)
            $.each(response.data, function(index, value){
                $(dest_elem).append("<div class='searched-song'><iframe id='ytplayer' class='player-thumbnail' type='text/html', width='280' height='180' src='http://www.youtube.com/embed/" + value['video_id'] + "' frameborder='0'></iframe><p>"+value['video_title']+"</p><button type='button' onclick='add_song(\"" + value['video_id'] +"\", \"" + value['video_title'] + "\")'><img class='icon add' src='./static/image/plus.svg'/>플레이리스트에 추가</button></div>");
            });
        }).fail(function() {
            $(dest_elem).text("Error: Could not contact server");
        });
    });
    /*
    var source = new EventSource("{{ url_for('sse.stream') }}");
    source.addEventListener('greeting', function(event) {
        var data = JSON.parse(event.data);
            console.log(data);
    }, false)
    */    
});
