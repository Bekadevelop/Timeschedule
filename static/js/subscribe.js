const vapidPublicKey = "{{ vapid_public_key }}";

if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/static/js/sw.js").then(function (registration) {
        return registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(vapidPublicKey),
        });
    }).then(function (subscription) {
        return fetch("{% url 'subscribe_to_push' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}",
            },
            body: JSON.stringify(subscription),
        });
    }).then(function (response) {
        if (!response.ok) {
            throw new Error("Failed to subscribe user.");
        }
        return response.json();
    }).then(function (data) {
        console.log("User subscribed:", data);
    }).catch(function (error) {
        console.error("Error during subscription:", error);
    });
}

function urlBase64ToUint8Array(base64String) {
    const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/");
    const rawData = window.atob(base64);
    return Uint8Array.from([...rawData].map((char) => char.charCodeAt(0)));
}
