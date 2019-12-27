var express = require('express');
var app = express();
var bodyParser = require('body-parser');

var urlencodedParser = bodyParser.urlencoded({ extended: false })//şifrelenmemiş
app.use(bodyParser.json())

app.use(express.static('templates'));

app.get('/home.html', function (req, res) {
    res.sendFile(__dirname + "/" + "home.html");
})

app.post('/predict', urlencodedParser, function (req, res) {

    var data = req.body;
    var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/predict";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");


    data = JSON.stringify(data);
    console.log("Sending:" + data);
    xhr.send(data);//json gönderildi

    xhr.onreadystatechange = function () {

        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            console.log("Python API Response:" + JSON.stringify(json));
            res.send(JSON.stringify(json));
        }
    };
})
app.post('/index',urlencodedParser, function (req, res) {

    var data = req.body;
    console.log(data);
    var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/index";

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    data = JSON.stringify(data);
	console.log("Sending:" +data);
	xhr.send(data);

     xhr.onreadystatechange = function () {

        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            console.log("Python API Response:" + JSON.stringify(json));
            res.send(JSON.stringify(json));
            //document.getElementById("prediction").innerHTML = JSON.stringify(json);

        }
    };
})


var server = app.listen(8081, function () {
    var host = server.address().address
    var port = server.address().port
    console.log("Example app listening at http://%s:%s", host, port)
})