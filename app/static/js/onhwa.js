function add_song(video_id, video_title) {
    edit_playlist(video_id, video_title, 'add');
}

function remove_song(video_id) {
    edit_playlist(video_id, '', 'remove');
}

function edit_playlist(video_id, video_title, mode) {
    //console.log(video_id);
    $.post('/edit_playlist', {
        video_id: video_id,
        video_title: video_title,
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
        $('#playlist').append("<li class='added-song' id='" + value['video_id'] + "'><img class='icon play-white' src='./static/image/play-white.svg' onclick='play_video(\"" + value['video_id'] + "\")'/><img class='icon pause-white' onclick='pause()' src='./static/image/pause-white.svg'/><img class='thumbnail' src='http://img.youtube.com/vi/" + value['video_id'] + "/default.jpg'><p class='title'>" + value['video_title'] + "</p><img class='icon trash' src='static/image/trash.svg' onclick='remove_song(\"" + value['video_id'] + "\")'/></li>");
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

function load_requests() {
    $.get('/get_requests', function(requests) {
        $('#requests').html('')
        $.each(requests.data, function(index, request) {
            var requester = request['requester'];
            var title = request['title'];
            var artist = request['artist'];
            $('#requests').append("<li class='pending-request'><p class='requester'>" + requester + "</p><p class='artist'>" + artist + "</p><p class='title'>" + title + "</p><img class='icon trash' src='static/image/trash.svg' onclick='remove_request(" + index + ")'/></li>");
            // call remove_request(index) to remove one request 
            // call search_request(artist, title) to search
        });
    });
}

function remove_request(index) {
    console.log('remove_request');
    //remove one request with index 'index'
}

function search_request(artist, title) {
    search_youtube(artist + ' ' + title);
}

function search_youtube(query) {
    console.log('search youtube');
    var dest_elem = $('#search_result');
    $(dest_elem).text('loading...');
    $.post('/search_youtube', {
        query: query
    }).done(function(response) {
        $(dest_elem).html('');
        $.each(response.data, function(index, value) {
            $(dest_elem).append("<div class='searched-song'><iframe id='ytplayer' class='player-thumbnail' type='text/html', width='280' height='180' src='https://www.youtube.com/embed/" + value['video_id'] + "' frameborder='0'></iframe><p>" + value['video_title'] + "</p><button type='button' onclick='add_song(\"" + value['video_id'] + "\", \"" + value['video_title'] + "\")'><img class='icon add' src='./static/image/plus.svg'/>플레이리스트에 추가</button></div>");
        });
    }).fail(function() {
        $(dest_elem).text("Error: Could not contact server");
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

    loadVideo();
    load_requests();

    /*
    var source = new EventSource("{{ url_for('sse.stream') }}");
    source.addEventListener('greeting', function(event) {
        var data = JSON.parse(event.data);
            console.log(data);
    }, false)
    */
});