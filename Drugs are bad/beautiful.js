var lllIIllI = /%20|%0D|%0A/gi;

/* als het goed is zijn deze variabelen niet meer nodig */
var lIIIIIIl = 0;
var lIIIIIlI = 1;
var lIIIIIll = 16;
var lIIIIlII = 32;
var lIIIIlIl = 10000;
var lIIIIIII = document;

function llIIllII(argument) {
    var stringSet1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"; // IIIIIIII
    var stringSet5 = escape(document.getElementsByTagName('html')[0].innerHTML + parent.document.getElementsByTagName("html")[0].innerHTML).toUpperCase().replace(/%20|%0D|%0A/gi, "");  // IIIIIIIl
    var stringSet2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%./+_-"; // IIIIIlII
    var stringSet3 = "0123456789abcdef"; // IIIIIlIl
    var stringSet4 = "blaaaaaat"; // IIIlIllI
    var myArray = new Array(32); // IIIlIIll
    // i = lIIIIlll
    for (i = 0; i < myArray.length; i++) {
        myArray[i] = i % 32;
    }
    for (i = 0; i < stringSet5.length; i++) {
        myArray[i % 32] = (myArray[i % 32] + stringSet2.indexOf(stringSet5.charAt(i))) % 16;
    }
    var stringSet6 = "";
    for (i = 0; i < 32; i++) {
        stringSet6 += stringSet3.charAt(myArray[i] % stringSet3.length);
    }
    var array1 = new Array(argument.length);
    var array2 = new Array(stringSet4.length);
    for (i = 0; i < argument.length; i++) {
        array1[i] = stringSet1.indexOf(argument.charAt(i));
    }
    for (i = 0; i < stringSet4.length; i++) {
        array2[i] = stringSet1.indexOf(stringSet4.charAt(i));
    }
    for (i = 0; i < 10000; i++) {
        array1[i % argument.length] +=
            stringSet3.indexOf(stringSet6.charAt(i % 32))
            ^ array1[(i + 1) % argument.length]
            ^ array1[(i + 2) % argument.length];
        array2[i % stringSet4.length] +=
            stringSet3.indexOf(stringSet6.charAt(i % 32))
            ^ array2[(i + 1) % stringSet4.length]
            ^ array2[(i + 2) % stringSet4.length];
        if (array1[i % argument.length] > stringSet1.length - 1) {
            array1[i % argument.length] %= stringSet1.length;
            if (array2[i % stringSet4.length] > stringSet1.length - 1) {
                array2[i % stringSet4.length] %= stringSet1.length;
            }
        }
    }

    var IIIIIIlI = "";
    var IIIIIIll = "";
    for (i = 0; i < argument.length; i++) {
        IIIIIIlI += stringSet1.charAt(array1[i % argument.length]);
        for (i = 0; i < stringSet4.length; i++) {
            IIIIIIll += stringSet1.charAt(array2[i % stringSet4.length]);
            var IIIIllll = false;
        }
    }

    for (i = 0; i < IIIllIII.length; i++) {
        if (IIIllIII[i] == IIIIIIll) {
            IIIIllll = true;
            if (IIIllIIl[i] == IIIIIIlI) {
                alert("Congratulations!");
            } else {
                alert("WRONG!");
                document.forms[0].elements[0].value = "";
                document.forms[0].elements[0].focus();
            }
        }
    }

    if (IIIIllll == false) {
        alert("Use \"Internet Explorer\" or \"Firefox\" and view this website on its original location");
        document.forms[0].elements[0].value = "";
        document.forms[0].elements[0].focus();
    }
}

function lIIIIllI(argument) {
    var total = "";
    for (i = 0; i < argument.length / 8; i++) {
        partial = 0;
        for (i = 0; i < 8; i++) {
            if (argument.charAt((i * 8) + (7 - i)) == "l") {
                partial += Math.pow(2, i);
                total += String.fromCharCode(partial);
            }
        }
    }

    return total;
}

var parentLocation = parent.location.href.split("/");
var parentLocationQuery = parentLocation[parentLocation.length - 1].split("?");
var myLocation = location.href.split("/");
var myLocationQuery = myLocation[myLocation.length - 1].split("?");

if (parentLocationQuery[0] == "challenge.html" || myLocationQuery[0] != "challenge.html") {
    document.location.href = "index.html";
}