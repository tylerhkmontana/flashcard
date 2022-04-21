const wordset_container = document.getElementById('wordset_container')
const words = wordset_container.children
const testset = []

for(i=0; i < words.length; i++) {
    var word = {
        name: words[i].childNodes[1].innerHTML,
        description: words[i].childNodes[3].innerHTML
    }

    testset.push(word)
}

// We need to shuffle the array
function shuffleArray(array) {
    // shuffle logic
}

// Make the logic to test the user with some timer