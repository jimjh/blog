Date: 2013-08-21
Title: How to Create a Websocket Server in Ruby
Category: Software
Tags: ruby

This is a short tutorial on creating a websocket server in Ruby using James Coglan's [websocket driver](https://github.com/faye/websocket-driver-ruby). The complete example is available on [github](https://github.com/jimjh/echo-websocket/blob/master/server.rb).

### About Websocket Driver

The [websocket-driver](http://rubygems.org/gems/websocket-driver) gem decouples the websocket protocol from the I/O layer, providing drivers that handle the websocket procotol (handshakes, upgrades etc) on any compatible I/O. It can be used with Rack, EventMachine, or just plain TCP. The examples for EventMachine and Rack are available in the documentation.

#### Using Plain TCP
This echo server was adapted from code found in poltergeist. It defines an `EchoServer` class, which is used as follows

    :::ruby
    server = EchoServer.new
    server.listen  # blocking

Within `#listen`, the server accepts clients connections in a continuous loop and spins off new threads to handle each client. The connected socket is passed to `WebSocket::Driver#server`, which selects, instantiates, and returns an appropriate driver.

    :::ruby
    driver = ::WebSocket::Driver.server(socket)
    driver.on(:connect) { driver.start }
    driver.on(:message) { |e| driver.text e.data }
    driver.on(:close)   { puts "Connection with #{socket.addr[2]} closed." }
    loop do
      IO.select([socket], [], [], 30) or raise Errno::EWOULDBLOCK
      data = socket.recv(RECV_SIZE)
      break if data.empty?
      driver.parse data
    end
    
In general, data received on the socket should be passed to `driver#parse`, and `driver#text` or `driver#bytes` can be used to send data to the other end. The echo server can be tested from any modern browser with the following JavaScript snippet.

    connection = new WebSocket('ws://localhost:54398/');
    // Log errors
    connection.onerror = function (error) { console.log('WebSocket Error ' + error); };
    // Log messages from the server
    connection.onmessage = function (e) { console.log('Server: ' + e.data); };