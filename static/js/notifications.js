const socket = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    alert("New Notification: " + data.message);
};

function sendNotification() {
    socket.send(JSON.stringify({ message: "Test notification!" }));
}
function sendNotification() {
    fetch('/api/notifications/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is included
        },
        body: JSON.stringify({
            'message': 'Test Notification'
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Notification sent:', data);
    })
    .catch((error) => {
        console.error('Error sending notification:', error);
    });
}
