



//function previousElementSibling(elem) {
//  do {
//    elem = elem.previousSibling;
//   } while ( elem && elem.nodeType !== 1 );
//    return elem;
//}

//function nextElementSibling(elem) {
//  do {
//    elem = elem.nextSibling;
//   } while ( elem && elem.nodeType !== 1 );
//    return elem;
//}
function displayChapters(trackElement){
  if ((trackElement.readyState == 2) && (textTrack = trackElement.track)){
        if(textTrack.kind === "chapters"){
            textTrack.mode = 'hidden';
            for (var i = 0; i < textTrack.cues.length; ++i) {
                var cue = textTrack.cues[i],
                chapterName = cue.text,
                start = cue.startTime,
                //newLocale = document.createElement("li"),
                location = document.createElement("a");
                //newLocale.setAttribute('class','item');
                location.setAttribute('id', start);
                location.setAttribute('tabindex', '0');
                location.setAttribute('class','item');
                var localeDescription = document.createTextNode(cue.text);
                location.appendChild(localeDescription);
                //newLocale.appendChild(location);
                locationList.appendChild(location)//newLocale); 
                location.addEventListener("click", 
                function() {
                	video.currentTime = this.id;
                }, false);
                
            }
          textTrack.addEventListener("cuechange",
		   function() {
                var currentLocation = this.activeCues[0].startTime;
                if (chapter = document.getElementById(currentLocation)) {
                	var locations = [].slice.call(document.querySelectorAll("#chapters a"));
                	for (var i = 0; i < locations.length; ++i) { locations[i].classList.remove("current"); }
                    chapter.classList.add("current");
                    // chapter.scrollIntoView();
            //locationList.style.top = "-"+chapter.parentNode.offsetTop+"px";
                }
            },
            false);
        
        }
    }
}

locationList = document.getElementById("chapters"),
video = document.getElementById("video-chapters"),
trackElement = video.getElementsByTagName("track")[0],
//displayChapters(trackElement);

video.addEventListener("loadedmetadata", function run_tests() {
    if (trackElement.readyState == 1) { setTimeout(run_tests, 1); } else { displayChapters(trackElement); }
})