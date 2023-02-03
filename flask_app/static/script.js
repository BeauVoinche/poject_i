MCU_URL = "https://mcuapi.herokuapp.com/api/v1/movies/"
resultsDiv = document.getElementById("infoResults")
phrase = "Hello, this is Jarvis, I am here to help you with your journey through the Marvel Cinematic Universe. Please cycle through the options here, and click on the tabs below it to get information about the film.";
phrase2 = "Ah yes, this will give give you a shortened explanation of the film selected.";
phrase3 = "Excellent choice, this gives you very interesting information about the film selected.";
target = document.getElementById("target");
target2 = document.getElementById("target2");
target3 = document.getElementById("target3");
i = 0;
j =0;
k=0;


function clearInfoDiv() {
    resultsDiv.innerHTML = `<p> </p>`
}

function typeOut() {
    if (i < phrase.length) {
        target.innerHTML += phrase.charAt(i);
        i++;
        setTimeout(typeOut, 80);
    }
}
if (window.attachEvent) { window.attachEvent('onload', typeOut());}
else if (window.addEventListener) { window.addEventListener('load', typeOut(), false); }
else { document.addEventListener('load', typeOut(), false); }


function typeOut2() {
    if (j < phrase2.length) {
        target2.innerHTML += phrase2.charAt(j);
        j++;
        setTimeout(typeOut2, 80);
    }
}


function typeOut3() {
    if (k < phrase3.length) {
        target3.innerHTML += phrase3.charAt(k);
        k++;
        setTimeout(typeOut3, 80);
    }
}


function getMoviePlot(p) {
    event.preventDefault();
    var movievalue = p.id
        fetch(MCU_URL + movievalue)
            .then(function (someServerResponse) {
                return someServerResponse.json()
            })
            
            .then(function (data) {
                console.log(data)
                resultsDiv.innerHTML = `
                <p> ${data.overview} </p>
                `
            })
            .catch((err) => {
                console.log("Houston we have a problem!", err)
            })
}


function getMovieInfo(p) {
    event.preventDefault();
    var movievalue = p.id
    fetch(MCU_URL + movievalue)
        .then(function (someServerResponse) {
            return someServerResponse.json()
        })
        .then(function (data) {
            console.log(data)
            var date_str = data.release_date;
            var date_list = date_str.split("-");
            var month;
            switch (date_list[1]) {
                case "01":
                    month = "January";
                    break;
                case "02":
                    month = "February";
                    break;
                case "03":
                    month = "March";
                    break;
                case "04":
                    month = "April";
                    break;
                case "05":
                    month = "May";
                    break;
                case "06":
                    month = "June";
                    break;
                case "07":
                    month = "July";
                    break;
                case "08":
                    month = "August";
                    break;
                case "09":
                    month = "September";
                    break;
                case "10":
                    month = "October";
                    break;
                case "11":
                    month = "November";
                    break;
                case "12":
                    month = "December";
                    break;
            }
            var new_date = month + " " + date_list[2] + ", " + date_list[0];
            resultsDiv.innerHTML = `
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Directed by:</th>
                            <th>Release Date:</th>
                            <th>Phase:</th>
                            <th>Saga:</th>
                            <th>Run Time:</th>
                            <th>Trailer:</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>${data.directed_by}</td>
                            <td>${new_date}</td>
                            <td>${data.phase}</td>
                            <td>${data.saga}</td>
                            <td>${data.duration} minutes</td>
                            <td><a href="${data.trailer_url}">${data.title}</a></td>
                        </tr>
                    </tbody>
                </table>
            `
        })
        .catch((err) => {
            console.log("Houston we have a problem!", err)
        })
}