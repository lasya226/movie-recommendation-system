function getRecommendations() {
    let movie = document.getElementById("movieSelect").value;

    fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "movie=" + movie
    })
    .then(res => res.json())
    .then(data => {
        let list = document.getElementById("results");
        list.innerHTML = "";
        data.forEach(m => {
            list.innerHTML += `<li>${m}</li>`;
        });
    });
}