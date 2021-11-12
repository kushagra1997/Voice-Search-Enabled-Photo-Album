if (!('webkitSpeechRecognition' in window)) {
  //Speech API not supported here…
  console.log("huh")
} else { //Let’s do some cool stuff :)
  var recognition = new webkitSpeechRecognition(); //That is the object that will manage our whole recognition process. 
  recognition.continuous = true;   //Suitable for dictation. 
  //recognition.interimResults = true;  //If we want to start receiving results even if they are not final.
  //Define some more additional parameters for the recognition:
  recognition.lang = "en-US"; 
  recognition.maxAlternatives = 1; //Since from our experience, the highest result is really the best...
  var recordButton = document.getElementById("recordButton");
  var stopButton = document.getElementById("stopButton");

  //add events to those 2 buttons
  recordButton.addEventListener("click", start);
  stopButton.addEventListener("click", end);

  function start(){
    console.log("recordButton clicked");
    recognition.start();
    recognition.onstart = function() {
    //Listening (capturing voice from audio input) started.
    //This is a good place to give the user visual feedback about that (i.e. flash a red light, etc.)
    recordButton.disabled = true;
    stopButton.disabled = false;
  };

}

function end(){
  console.log("stopButton clicked");
  recognition.stop();
  recognition.onend = function() {
      //Again – give the user feedback that you are not listening anymore. If you wish to achieve continuous recognition – you can write a script to start the recognizer again here.
      stopButton.disabled = true;
      recordButton.disabled = false;
    
  };

  recognition.onresult = function(event) { //the event holds the results
  //Yay – we have results! Let’s check if they are defined and if final or not:
      if (typeof(event.results) === 'undefined') { //Something is wrong…
          recognition.stop();
          return;
      }

      for (var i = event.resultIndex; i < event.results.length; ++i) {      
          if (event.results[i].isFinal) { //Final results
              console.log("final results: " + event.results[i][0].transcript);   //Of course – here is the place to do useful things with the results.
              document.getElementById("transcript").value = event.results[i][0].transcript;
          } else {   //i.e. interim...
              console.log("interim results: " + event.results[i][0].transcript);  //You can use these results to give the user near real time experience.
          } 
      } //end for loop
  }; 

}

}