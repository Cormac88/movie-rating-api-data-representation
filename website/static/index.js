function search(evt) {
  // We create a request to the home endpoint with a vlaue of the input as the body.
  fetch("/", {
    method: "POST",
    body: JSON.stringify({ search: evt.value }),
  })
    .then((res) => res.json())
    .then((data) => {
      // After parsing the data we clear the previous list.
      // Then map over the results of the API call.
      // And create links to the /movie endpoint with the movie id passed as a query parameter.
      const list = document.getElementById("list");
      list.innerHTML = "";
      data.results.map((result) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = `/movie?id=${result.id}`;
        a.innerHTML = result.original_title;
        li.appendChild(a);
        list.appendChild(li);
      });
    });
}

// 🕺🕺 
function playMusic() {
  const track = document.getElementById("audio");
  track.play();
}

// Here we style the background of the body. A colour yellow based on how much "butter" a user has given the movie.
// More butter is better!
function butterMeUp(evt){
  const butter = (Math.abs(evt.value - 100) / 100 ) * 255
  document.body.style.background = `rgb(255, 255, ${butter})`
}