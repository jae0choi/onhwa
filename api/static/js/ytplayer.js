// reference : https://developers.google.com/youtube/iframe_api_reference
// 2. This code loads the IFrame Player API code asynchronously.

function init_player(){
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}
// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
var current_video_index;

function onYouTubeIframeAPIReady() {
    current_video_index = 0;
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: video_ids[current_video_index],
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange,
            'onError': onPlayerError
        }
    });
}

function play_video_at(index){
    load_player_with_id(index);
}
function load_player_with_id(index){
    player.loadVideoById(video_ids[index]);
    var iframe = $('#player');
    var src = iframe.attr('src');
    var res = src.split('?')[0];
    res += ' frameborder="0" allowfullscreen'

}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {

    event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED){
        nextVideo();
    }
}
function onPlayerError(event){
    // nextVideo();
}

function getNextIndex(cur_index){
    return cur_index+1
}
function getPrevIndex(cur_index){
    return cur_index-1
}
function nextVideo() {
    if (player) {
        new_video_index = getNextIndex(current_video_index);
        number_of_videos = video_ids.length;

        if (new_video_index == number_of_videos){
            new_video_index = 0;
        }
        current_video_index = new_video_index;
        load_player_with_id(new_video_index);
    }
}

function prevVideo(){
    if (player) {
        new_video_index = getPrevIndex(current_video_index);
        if (new_video_index == -1){
            number_of_videos = video_ids.length;
            new_video_index = number_of_videos - 1;
        }
        current_video_index = new_video_index;
        load_player_with_id(new_video_index);
    }
}

function play() {
    if (ytplayer) {
        ytplayer.playVideo();
    }
}
function pause() {
    if (ytplayer) {
        ytplayer.pauseVideo();
    }
}
function stopVideo() {
    player.stopVideo();
}