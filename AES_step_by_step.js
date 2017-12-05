var ct = atob(document.getElementById("ciphertext").innerHTML);
var ctArray = [].map.call(ct, x=>x.charCodeAt(0));


String.fromCharCode(...ctArray)

ajax(
    btoa(String.fromCharCode(...ctArray)))
	




var idx = ct.length - 17;

ajax(
    btoa(String.fromCharCode(...ctArray)),
    function(x){console.log("found: " + x)},
    79 );
	
var i = 0;
while (i < 0xFF ){
	ctArray[idx] = i;
	ajax(
		btoa(String.fromCharCode(...ctArray)),
		function(x){console.log("found: " + x)},
		i );
	i++;
}