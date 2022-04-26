function parseCookie(cookie){
    return cookie
    .split(';')
    .map(v => v.split('='))
    .reduce((acc, v) => {
      acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
      return acc;
    }, {});
}
const parsedCookie = parseCookie(document.cookie)
const testset = JSON.parse(parsedCookie.testset)

const printScore = (testset) =>{
    let correct = 0;
    testset.forEach(word => {
        if(word.result == "correct"){
            correct++;
        }
    });
    let percentage = correct / testset.length
    //print score
    document.getElementById("score").innerHTML = correct + "/" + testset.length
    //print percentage
    console.log(percentage)
    document.getElementById("percentage").innerHTML = percentage.toFixed(2) * 100 + "%"
    //print Incorrect words
    for(let i=0; i<testset.length; i++){
        if(testset[i].result == "incorrect"){
            let word_container = document.createElement("div")
            word_container.setAttribute("class", "word_container")
            let incorrect_word = document.createElement("h2")
            incorrect_word.innerHTML = testset[i].name
            let incorrect_word_desc = document.createElement("p")
            incorrect_word_desc.innerHTML = testset[i].description
            word_container.appendChild(incorrect_word)
            word_container.appendChild(document.createElement("hr"))
            word_container.appendChild(incorrect_word_desc)
            document.getElementById("incorrect_words").appendChild(word_container)
        }
    }
}

printScore(testset)