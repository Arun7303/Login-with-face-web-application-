let video;
let canvas;
let nameInput;

function init() {
    video = document.getElementById("video");
    canvas = document.getElementById("canvas");
    nameInput = document.getElementById("name");

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.onloadedmetadata = () => {
                video.play();
                // Call capture() when the video stream is ready
                capture();
            };
        })
        .catch(error => {
            console.error("Error accessing webcam", error);
            alert("Cannot access webcam");
        });
}

function capture() {
    let context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    // Request the next frame
    requestAnimationFrame(capture);
}

function register() {
    const name = nameInput.value;
    const photo = dataURItoBlob(canvas.toDataURL());
    if (!name || !photo) {
        alert("Name and photo required, please.");
        return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("photo", photo, `${name}.jpg`);

    fetch("/register", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Data successfully registered.");
                window.location.href = "/";
            } else {
                alert("Sorry, registration failed.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function login() {
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const photo = dataURItoBlob(canvas.toDataURL());

    if (!photo) {
        alert("Photo required, please.");
        return;
    }

    const formData = new FormData();
    formData.append("photo", photo, "login.jpg");

    fetch("/login", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.success) {
            alert("Login success!");
            // Redirect or perform other actions upon successful login
        } else {
            alert("Login failed. Please try again.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(",")[1]);
    const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mimeString });
}

init();
