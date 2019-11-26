
$(function(){
    $('#video-chapters').on('loadedmetadata', function(){
        var track = document.getElementById('chapters-track');
        var video = document.getElementById('video-chapters');
        var menuChapters = document.getElementById("chapters-menu");
        $('#chapters-container div.loading').hide();
        console.log('se cargo #video-chapters');
        if (track.kind === 'chapters'){
            track.track.mode = 'hidden';
            for (var i = 0; i < track.track.cues.length; ++i){
                cue = track.track.cues[i];
                chapterItem = document.createElement('a');
                chapterItem.setAttribute('id', cue.startTime);
                chapterItem.setAttribute('tabindex', '0');
                chapterItem.setAttribute('class','item');
                chapterName = document.createTextNode(cue.id);
                chapterItem.appendChild(chapterName);
                chapterItem.addEventListener('click', 
                function() {
                    video.currentTime = this.id;
                }, false);
                menuChapters.appendChild(chapterItem);
            }
            track.track.addEventListener('cuechange',
                function(){
                    var currentChapter = this.activeCues[0].startTime;
                    if (chapter = document.getElementById(currentChapter)){
                        var items = [].slice.call(document.querySelectorAll("#chapters-menu a"));
                        var entrydeschap = document.getElementById("entry-desc-chap");
                        for (var i = 0; i < items.length; ++i) { 
                            items[i].classList.remove("active");
                            var chapterdesc = document.createTextNode(this.activeCues[0].text);
                            $('#sec-num').text(this.activeCues[0].id);
                            entrydeschap.removeChild(entrydeschap.lastChild);
                            entrydeschap.appendChild(chapterdesc);
                        }
                        chapter.classList.add("active");
                    }
                }, false
            );
        }
    });
});

