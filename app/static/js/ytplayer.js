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
var current_video_id;
var video_ids;

function onYouTubeIframeAPIReady() {
    current_video_id = video_ids[0];
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: current_video_id, 
        controls: false,
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange,
            'onError': onPlayerError
        }
    });
    status_update();
}

function play_video(video_id){
    current_video_id = video_id;
    load_player_with_id(video_id);
}

function load_player_with_id(video_id){
    player.loadVideoById(video_id);
    var iframe = $('#player');
    var src = iframe.attr('src');
    var res = src.split('?')[0];
    res += ' frameborder="0" allowfullscreen'
    status_update();
}

function remove_playing(){
    $('#playlist li').each(function(index){
        if ($(this).hasClass("playing")){
            $(this).removeClass("playing");
        }
    });
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
    nextVideo();
}

function getCurrentIndex(){
    return video_ids.indexOf(current_video_id)
}
function getNextIndex(){
    new_video_index = getCurrentIndex()+1;
    number_of_videos = video_ids.length;
    if (new_video_index == number_of_videos){
        new_video_index = 0;
    } 
    return new_video_index
}
function getPrevIndex(){
    new_video_index = getCurrentIndex()-1;
    if (new_video_index == -1){
            number_of_videos = video_ids.length;
            new_video_index = number_of_videos - 1;
    }
    return new_video_index
}
function nextVideo() {
    if (player) {
        new_video_id = video_ids[getNextIndex()];
        current_video_id = new_video_id;
        load_player_with_id(new_video_id);
    }
}

function prevVideo(){
    if (player) {
        new_video_id = video_ids[getPrevIndex()];
        
        current_video_id = new_video_id;
        load_player_with_id(new_video_id);
    }
}

function play() {
    if (player) {
        player.playVideo();
    }
}
function pause() {
    if (player) {
        player.pauseVideo();
        remove_playing();
    }
}
function stopVideo() {
    player.stopVideo();
}