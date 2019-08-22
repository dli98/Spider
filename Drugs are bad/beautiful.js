var lllIIllI = /%20|%0D|%0A/gi;

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
    var array1 = new Array(9);
    var array2 = new Array(9);
    for (i = 0; i < 9; i++) {
        array1[i] = stringSet1.indexOf(argument.charAt(i));
    }
    for (i = 0; i < 9; i++) {
        array2[i] = stringSet1.indexOf(stringSet4.charAt(i));
    }
    for (i = 0; i < 10000; i++) {
        array1[i % 9] +=
            stringSet3.indexOf(stringSet6.charAt(i % 32))
            ^ array1[(i + 1) % 9]
            ^ array1[(i + 2) % 9];
        array2[i % 9] +=
            stringSet3.indexOf(stringSet6.charAt(i % 32))
            ^ array2[(i + 1) % 9]
            ^ array2[(i + 2) % 9];
        if (array1[i % 9] > 61) {
            array1[i % 9] %= 62;
        }
        if (array2[i % 9] > 61) {
            array2[i % 9] %= 62;
        }
    }

    var IIIIIIlI = "";
    var IIIIIIll = "";
    for (i = 0; i < 9; i++) {
        //0KhEoB9M5 <-- [ 48, 75, 104, 69, 111, 66, 57, 77, 53 ] <-- array1[]
        //qLMsjYygK <-- [ 113, 76, 77, 115, 106, 89, 121, 103, 75 ] <-- array1[]
        // <-- password length = 9
        IIIIIIlI += stringSet1.charAt(array1[i % 9]);
    }
    for (i = 0; i < 9; i++) {
        // aftCP0szE <-- [ 97, 102, 116, 67, 80, 48, 115, 122, 69 ] <-- array2[]
        // 2Qo4CxJXP <-- [ 50, 81, 111, 52, 67, 120, 74, 88, 80 ] <-- array2[]
        IIIIIIll += stringSet1.charAt(array2[i % 9]);

    }
    var IIIIllll = false;
    // IIIllIII[0] = "aftCP0szE";
    // IIIllIII[1] = "2Qo4CxJXP";
    for (i = 0; i < 2; i++) {
        if (IIIllIII[i] == IIIIIIll) {
            IIIIllll = true;

            // IIIllIIl[0] = "0KhEoB9M5";
            // IIIllIIl[1] = "qLMsjYygK";
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
    for (i = 0; i < 9 / 8; i++) {
        partial = 0;
        for (i = 0; i < 8; i++)
            if (argument.charAt((i * 8) + (7 - i)) == "l")
                partial += Math.pow(2, i);
        total += String.fromCharCode(partial);
    }
    return total;
}

// "http://www.net-force.nl/challenge/level108/index.html"
var parentLocation = parent.location.href.split("/");
// index.html
var parentLocationQuery = parentLocation[parentLocation.length - 1].split("?");
// location.href "http://www.net-force.nl/challenge/level108/challenge.html"
var myLocation = location.href.split("/");
// challenge.html
var myLocationQuery = myLocation[myLocation.length - 1].split("?");

if (parentLocationQuery[0] == "challenge.html" || myLocationQuery[0] != "challenge.html") {
    document.location.href = "index.html";
}