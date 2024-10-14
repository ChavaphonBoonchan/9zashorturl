document.getElementById('urlForm').addEventListener('submit', function (e) {
    e.preventDefault();
    
    const longUrl = document.getElementById('longUrl').value;

    fetch('/shorten', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ longUrl })
    })
    .then(response => response.json())
    .then(data => {
        const shortUrlDiv = document.getElementById('shortenedUrl');
        shortUrlDiv.innerHTML = `Shortened URL: <a href="${data.shortUrl}">${data.shortUrl}</a>`;
    });
});
