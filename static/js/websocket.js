let socket; // Declare the variable

function initializeWebSocket() {
    if (!socket) { // Check if it's already initialized
        socket = new WebSocket("ws://localhost:8000/ws/notifications/");

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            console.log("New Notification:", data.message);
            // You can also update the UI to display the notification here
        };

        socket.onopen = function() {
            console.log("WebSocket Connected");
        };

        socket.onclose = function() {
            console.log("WebSocket Disconnected");
        };
    }
}

initializeWebSocket(); // Call the function to initialize the WebSocket
