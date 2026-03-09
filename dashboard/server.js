const express = require('express')
const fs = require('fs');
const path = require('path');
const body_parser = require("body-parser");
const app = express();
//express  can only handle one way connections
//it cannot handle two way connections
//so to handle a permenant connection we need https server
//so when that req comes it has a header with upgrade key
// http wrapper sees it and hand off that to socket .io
//this http wrapper decides konsi req express ko deni konsi socket ko
const http = require('http').Server(app);
const io = require('socket.io')(http);

//  okay so basically we have 2 client server rs
// one is btw python and server (which basically act as a databsse and server)
// one is btw server and browser
// we receive data on Node
// now Browser can only ask , it cannot receive so instead of browser asking it again and again (polling), we establish a connection
// now node and broswer has a connection established
// node sends the data through sockets
// sockets trigger an event for which broswer is listening
// when the even is triggered , the front end code of browser handles the data packet 

app.use(express.static(path.join(__dirname,"public")));
app.use(body_parser.json());

app.get("/",(req,res,next)=>{
    console.log("URL",req.url, " Method",req.method);
    res.sendFile(path.join(__dirname,"views","index.html"));
})

app.post('/data',(req,res,next)=>{
    // console.log("post request");
    // console.log(req.body);
    io.emit('packet-arrived',req.body);
    res.sendStatus(200);
    
})

app.post('/ui-config',(req,res,next)=>{
    // console.log("post request");
    // console.log(req.body);
    io.emit('config-arrived',req.body);
    res.sendStatus(200);
    
})

app.post('/telemetry-config',(req,res,next)=>{
    // console.log("post request");
    // console.log(req.body);
    io.emit('telemetry-arrived',req.body);
    res.sendStatus(200);
    
})

const PORT = 3000;
http.listen(PORT,()=>{
    console.log(`server running at http://localhost:${PORT}`)
})