var sounds = [
			  "appconf.wav", "endclose.wav", "noidea.wav", "pitiable.wav", "whatmean.wav",
			  "asleep.wav",    "getbotom.wav",  "notposs.wav",   "planmut.wav",   "whatwant.wav",
			  "canttell.wav",  "gobbgook.wav",  "nottosay.wav",  "repriman.wav",  "wrngfut.wav",
			  "carefull.wav",  "goodbye.wav",   "outofmnd.wav",  "resist.wav",
			  "carryord.wav",  "intoller.wav",  "photread.wav",  "undwomen.wav",
			  "doubtsfl.wav",  "lveship.wav",   "picdism.wav",   "whatis.wav",
			 ]


function playSound(path){
	var myAudio = new Audio(path);
	myAudio.play();
}


function randomPlay(dir, name_list){	
	var idx = Math.floor( Math.random() * name_list.length )
	playSound(dir + name_list[idx])
}