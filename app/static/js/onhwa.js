var url_sse; // SSE
var array_requests = [];

function add_song(video_id, video_title, artist, title, requester) {
    edit_playlist(video_id, video_title, artist, title, requester, 'add');
}

function remove_song(video_id) {
    edit_playlist(video_id, '','','','', 'remove');
}

function edit_playlist(video_id, video_title, artist, title, requester, mode) {
    console.log(video_id, video_title, artist, title, requester );
    $.post('/edit_playlist', {
        video_id: video_id,
        video_title: video_title,
        artist: artist, 
        title: title, 
        requester: requester,
        mode: mode
    }).done(function(response) {
        console.log('Song edit success');
        update_playlist(response);
    }).fail(function() {
        console.log('Song edit failed');
    });
}

function update_playlist(playlist) {
    $('#playlist').html('')
    video_ids = [];

    $.each(playlist.data, function(index, value) {
        video_ids.push(value['video_id']);

        if(value['artist']){
            $('#playlist').append("<li class='added-song' id='" + value['video_id'] + "'><img class='icon play-white' src='./static/image/play-white.svg' onclick='play_video(\"" + value['video_id'] + "\")'/><img class='icon pause-white' onclick='pause()' src='./static/image/pause-white.svg'/><img class='thumbnail' src='https://img.youtube.com/vi/" + value['video_id'] + "/default.jpg'><div class='info-container'><div class='original-info'><p class='title'>[" + value['video_title'] + "]</p></div><div class='requester-info'><p class='requester'>" + value['requester'] + " 👉 </p><p class='artist'>" + value['artist'] + "</p>, <p class='song-title'>" + value['song_title'] + "</p></div></div><img class='icon trash' src='static/image/trash.svg' onclick='remove_song(\"" + value['video_id'] + "\")'/></li>");
        }else{
            $('#playlist').append("<li class='added-song' id='" + value['video_id'] + "'><img class='icon play-white' src='./static/image/play-white.svg' onclick='play_video(\"" + value['video_id'] + "\")'/><img class='icon pause-white' onclick='pause()' src='./static/image/pause-white.svg'/><img class='thumbnail' src='https://img.youtube.com/vi/" + value['video_id'] + "/default.jpg'><div class='info-container'><div class='original-info'><p class='title'>[" + value['video_title'] + "]</p></div></div><img class='icon trash' src='static/image/trash.svg' onclick='remove_song(\"" + value['video_id'] + "\")'/></li>");
        }
    });
    status_update();
}

function reorder_playlist() {
    $.post('/reorder_playlist', {
        video_ids: video_ids
    }).done(function(response) {
        console.log('video_ids push success');
        update_playlist(response)
    }).fail(function() {
        console.log('video ids push failed');
    });

}

function load_playlist() {
    $.get('/load_playlist', function(playlist) {
        update_playlist(playlist)

    });
}

function status_update() {
    $('#playlist li').each(function(index) {
        if ($(this).hasClass("playing")) {
            $(this).removeClass("playing");
        }
        if ($(this).hasClass("selected")) {
            $(this).removeClass("selected");
        }
        if (index == getCurrentIndex()) {
            $(this).addClass("playing");
            $(this).addClass("selected");
        }
    });
}

function export_playlist() {
    $.get('/export_playlist', function() {
        console.log('export playlist called');
    });
}

function remove_playlist(){
    $.get('/remove_playlist', function() {
        console.log('remove playlist');
        load_playlist();
    });
}

function remove_all_requests(){
    $.get('/remove_all_requests', function(){
        console.log('remove all requests');
        load_requests();
    });
}
function copy_playlist(){
    $.get('/copy_playlist', function(playlist) {
        console.log('copy playlist');
        const el = document.createElement('textarea');
        el.value = playlist;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
    });
}

function load_requests() {
    $.get('/get_requests', function(requests) {
        $('#requests').html('')
        $.each(requests.data, function(index, request) {
            var requester = request['requester'];
            var title = request['title'];
            var artist = request['artist'];
            $('#requests').append("<li class='pending-request request-form-"+ index + "'><div class='request-left' onclick='search_request(\"" + artist + "\", \"" + title + "\", \"" + requester + "\")'><p class='requester'>" + requester + "</p><span>:: </span><br><p class='artist'>" + artist + "</p><span>, </span><p class='title'>" + title + "</p></div><div class='request-right'><img class='icon trash2' src='static/image/trash.svg' onclick='remove_request(" + index + ");' /></li></div>");
            // call remove_request(index) to remove one request 
            // call search_request(artist, title) to search
            array_requests.push({'title': title, 'artist': artist, 'requester': requester});
        })
    });
}

function remove_request(index) {
    console.log('remove_request', index);
    var selector = '.request-form-' + index;
    req = array_requests[index];
    console.log(req);
    $.post('/remove_request', {
        title: req.title,
        artist: req.artist,
        requester: req.requester
    }).done(function(response){
        array_requests.splice(index,1);
        $(selector).remove();    
    }).fail(function(){
        console.log('Remove request failed');
    });
    //remove one request with index 'index' from db
}

function search_request(artist, title, requester) {
    console.log(artist + ' ' + title);
    search_youtube(artist, title, requester);
}

function search_youtube(query, title, requester) {
    console.log('search youtube');
    console.log(query);
    var artist;

    if(title){
        artist = query;
        var query = query + ' ' + title;
    }else{
        artist = '';
        title ='';
        var query = query;
    }
    console.log(query);
    // result open
    $('#search-result-container').css('display','block');
    
    var requester = (requester)? requester : '';
    
    var dest_elem = $('#search_result');
    $(dest_elem).text('loading...');
    $.post('/search_youtube', {
        query: query
    }).done(function(response) {

        $(dest_elem).html('');
        $.each(response.data, function(index, value) {
            
            $(dest_elem).append("<div class='searched-song'><iframe id='ytplayer' class='player-thumbnail' type='text/html', width='280' height='180' src='https://www.youtube.com/embed/" + value['video_id'] + "' frameborder='0'></iframe><p>" + value['video_title'] + "</p><button type='button' onclick='add_song(\"" + value['video_id'] + "\", \"" + value['video_title'].replace("/\"/gi","\'") + "\", \"" + artist + "\", \"" + title + "\", \"" + requester + "\")'><img class='icon add' src='./static/image/plus.svg'/>Add to playlist</button></div>");
        });
        
    }).fail(function() {
        $(dest_elem).text("Error: Could not contact server");
    });

}

function send_request_status(is_request_open){
    $.post('send_request_status', {
        is_request_open: is_request_open
    }).done(function(response){
        console.log('send_request_status');
    })
}

function check_open_for_request(){
    $.get('/check_open_for_request', function(requests){
        if (requests.data){
            //main.html
            $('#request-form-open').removeClass('hidden');
            $('#request-form-closed').addClass('hidden');

            //index.html
            $('#request_open_checkbox').attr('checked', true);
        }
        else{
            //main.html
            $('#request-form-open').addClass('hidden');
            $('#request-form-closed').removeClass('hidden');
            //iondex.html
            $('#request_open_checkbox').attr('checked',false);
        }
    });
}



$(document).ready(function() {
    init_player();
    load_playlist();

    $("#playlist").sortable({
        update: function(event) {
            //update playlist index
            var sorted_ids = $('#playlist').sortable("toArray");
            video_ids = sorted_ids;
            reorder_playlist();
            //      console.log('sortable to array');
            //      console.log(sorted_ids);
        }
    });
    $("#playlist").disableSelection();

    $('#search_youtube').submit(function(event) {
        event.preventDefault();
        search_youtube($('#query').val());
    });
    check_open_for_request();    
      
    $('#request_open_checkbox').change(function(){
        // if($(this).is(":checked")) {
        //     $('#request_open_textbox').html('신청곡 받는중');
        // } else{
        //     $('#request_open_textbox').html('신청곡 마감');
        // }
        send_request_status($(this).is(":checked"));
    });
    
    loadVideo();
    load_requests();
    //if ($('#playlist').length>0){ // is there a better way to distiguish parent html files? 
       
    //}
    /*
    var source = new EventSource("{{ url_for('sse.stream') }}");
    source.addEventListener('greeting', function(event) {
        var data = JSON.parse(event.data);
            console.log(data);
    }, false)
    */
});
