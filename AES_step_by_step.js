var ct = atob("D36vDR5/OvX4XO++/ZtA0t5bGZEYWFgvsqxLtY4pC8yWvu0bmeenJYCNLAViDV5Ap3n+3gGvm9HEbnwaZZabT+4iE7vKpIHblyr17Vj8BAI=");
var ctArray = [].map.call(ct, x=>x.charCodeAt(0));

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