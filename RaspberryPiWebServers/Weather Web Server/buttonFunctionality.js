//connect to the socket server.
var socket = io.connect('http://' + document.domain + ':' + 5000);


//receive message from server on 'serverToClientCurrently'
//change the heading text
socket.on('serverToClientCurrently', function(msg) {
    document.getElementById("currentTemp").innerText = "The Current Temperature in Burlington is " + msg.words + " *C";
        
   });
   
   //For Hourly Temp
socket.on('serverToClientHourly', function(msg) {
       
    document.getElementById("nowTemp").innerText = "The Current Temperature is " + msg.words[0] + " *C"; 
    document.getElementById("HourLater1").innerText = "The Temperature in 1 hour is " + msg.words[1] + " *C"; 
    document.getElementById("HourLater2").innerText = "The Temperature in 2 hours is " + msg.words[2] + " *C"; 
    document.getElementById("HourLater3").innerText = "The Temperature in 3 hours is " + msg.words[3] + " *C"; 
    document.getElementById("HourLater4").innerText = "The Temperature in 4 hours is " + msg.words[4] + " *C"; 
    document.getElementById("HourLater5").innerText = "The Temperature in 5 hours is " + msg.words[5] + " *C"; 
    document.getElementById("HourLater6").innerText = "The Temperature in 6 hours is " + msg.words[6] + " *C"; 
    document.getElementById("HourLater7").innerText = "The Temperature in 7 hours is " + msg.words[7] + " *C"; 
    document.getElementById("HourLater8").innerText = "The Temperature in 8 hours is " + msg.words[8] + " *C"; 
    document.getElementById("HourLater9").innerText = "The Temperature in 9 hours is " + msg.words[9] + " *C"; 
    document.getElementById("HourLater10").innerText = "The Temperature in 10 hours is " + msg.words[10] + " *C"; 
    document.getElementById("HourLater11").innerText = "The Temperature in 11 hours is " + msg.words[11] + " *C"; 

       
});
   
//For Daily Temp
socket.on('serverToClientDaily', function(msg) {
       
    document.getElementById("todayTemp").innerText = "The Temperature today is " + msg.words[0] + " *C"; 
    document.getElementById("tomorrowTemp").innerText = "The Temperature tomorrow is " + msg.words[1] + " *C";
    document.getElementById("DaysFutureTemp2").innerText = "The Temperature in 2 days is: " + msg.words[2] + " *C"; 
    document.getElementById("DaysFutureTemp3").innerText = "The Temperature in 3 days is: " + msg.words[3] + " *C"; 
    document.getElementById("DaysFutureTemp4").innerText = "The Temperature in 4 days is: " + msg.words[4] + " *C"; 
    document.getElementById("DaysFutureTemp5").innerText = "The Temperature in 5 days is: " + msg.words[5] + " *C"; 
    document.getElementById("DaysFutureTemp6").innerText = "The Temperature in 6 days is: " + msg.words[6] + " *C"; 
       
});
   
//when HTMl button is pressed, sends message to server from the client
function hourlyWeatherBurlingtonButton(){
    socket.emit('submit', "Hourly");
}
   
function dailyWeatherBurlingtonButton(){
    socket.emit('submit', "Daily");
}