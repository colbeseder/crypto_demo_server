//Solution
var inFlight = [];
function ping(data, cb, idx) {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "/AES_CBC_message");
	xhr.onreadystatechange = function () {
		if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
			cb(idx)
		}
	}
	inFlight.push(xhr);
	xhr.send(btoa(data));
}

function abortAll(){
	inFlight.map(x => x.abort());
	inFlight = [];
}

function letterReplace(str, newChar, idx){
	if (typeof newChar === "number"){
		newChar = String.fromCharCode(newChar);
	}
	return str.slice(0, idx) + newChar + str.slice(idx+1);
}

function findLastChar(enc){
	for (var i = 0 ; i < 0xFF; i++){
		ping(
			letterReplace(enc, i, enc.length - 17),
			function(x){console.log(x);},
			i );
	}
}

var ct = "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0" + atob(document.getElementById("ciphertext").innerHTML);
var raw = new Array(ct.length);
var pt = new Array(ct.length);;

function update(found, idx) {
	abortAll();
	var decoyPadding = 16 - (idx % 16);
	var C = found ^ decoyPadding;
	raw[idx] = C;
	pt[idx] = C ^ ct.charCodeAt(idx - 16);
	console.log(pt[idx]);
	console.log(String.fromCharCode(...pt));
	if (idx > 16){
		idx--;
		if (ct.length - idx > 16){
			ct = ct.slice(0, -16);
			idx = ct.length - 1;
		}
		findNextChar(idx);
	}
	else {
		console.log(String.fromCharCode(...pt));
	}
}

function findNextChar(idx){
	var decoyPadding = 16 - (idx % 16);
	var txt = ct.slice();
	for (i = ct.length -1 ; i > ct.length -16 && raw[i] != null ; i--){
		txt = letterReplace(txt, String.fromCharCode(decoyPadding ^ raw[i]) , i - 16);
	}

	for (var i = 0; i < 0xFF; i++) {
		var t;
		ping(
			letterReplace(txt, i, idx - 16),
			(function (found, real) {
				return function () {
					if (found === real && raw[idx] != null) {
						return;
					}
					else if (found === real){
						console.log("found === real");
						t = setTimeout(function(){
							update(found, idx);
						}, 2E3);
					}
					else {
						clearTimeout(t);
						update(found, idx);
					}
				}
			})(i, ct.charCodeAt(idx - 16))    );
	}

}

var idx = ct.length - 1;
findNextChar(idx);

