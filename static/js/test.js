const testset = []
let currentWord = null; // keep track of current word testing
const test_start_bt = document.getElementById('test_start_bt')
const test_skip_bt = document.getElementById('test_skip_bt')
let time_limit = 10; // time limit default = 10s
let time_out = null; // time_out variable to clear timeout

// set display style of word container to "none"
function setWordInvisible(id){
    document.getElementById(id).style.display = "none"
}

// Shuffle the array
function shuffleArray(array) {
    // Modern Fisher-Yates algorithm with O(n) time complexity and O(1) space complexity
    for (let i = array.length - 1; i > 0; i--) {// from last element, move to previous element
        let j = Math.floor(Math.random() * (i + 1)); // choose random index from 0 to i
        [array[i], array[j]] = [array[j], array[i]]; // swap it with the last element
    }
}

async function testWord(id, time_limit){
    // set current word
    currentWord = id

    // show the word
    toggleWordVisibility(id)
    
    // give limited time to take a test on word
    await timeout(time_limit)

    // when the time limit is passed, check the word description with input and empty input
    checkWord(id, document.getElementById(currentWord).querySelector('.description').value)
    document.getElementById(currentWord).querySelector('.description').value = ''

    // hide the word after test is finished
    toggleWordVisibility(id)
}

// check if the desciption of the word given id matches the input 
function checkWord(id, input){
    if(input == testset.find(word => word.id == id).description){
        testset.find(word => word.id == id).result = "correct"
    }else{
        testset.find(word => word.id == id).result = "incorrect"
    }
}

function toggleWordVisibility(id){
    document.getElementById(id).style.display = document.getElementById(id).style.display == "none" ? "flex" : "none"
}

function timeout (ms) {
    return new Promise(res => {time_out = setTimeout(res,ms)})
}

// set cookie with a testset array and send them to result page
function showResult(){
    document.cookie="testset=" + JSON.stringify(testset) + ";path=/result"
    window.location.href="../result"
}

// when enter button is clicked, run test on words that are not tested yet.
test_enter_bt.addEventListener('click', async (e) => {
    //check the word description with input and empty input
    checkWord(currentWord,document.getElementById(currentWord).querySelector('.description').value)
    document.getElementById(currentWord).querySelector('.description').value = ''

    // clearTimeout for previous timeout
    clearTimeout(time_out)

    // toggle previous word visibility before starting the next word
    toggleWordVisibility(currentWord)

    currentIndex = testset.indexOf(testset.find(word=>word.id == currentWord)) + 1 //Index of current word
    // Proceed the rest of the test
    time_limit = document.getElementById('time_limit').value || time_limit

    // run tests on words left
    for(let j=currentIndex; j<testset.length; j++){
        currentWord = testset[j].id
        await testWord(testset[j].id,time_limit*1000)
    }
    
    //show result only when test is done
    if(testset[testset.length-1].result != "pending"){
        showResult()
    }
})

// When test start button is clicked
test_start_bt.addEventListener('click', async (e) => {

    const wordset_container = document.getElementById('wordset_container')
    const words = wordset_container.children

    // initialize testset array and style
    for(i=0; i < words.length; i++) {
        if(words[i].className == "word_container"){
            var word = {
                id: words[i].childNodes[1].innerHTML,
                name: words[i].childNodes[3].innerHTML,
                description: words[i].childNodes[5].innerHTML,
                result: "pending"
            }
            testset.push(word)
            setWordInvisible(word.id)
        }
    }

    // hide setting and start button and show words
    document.getElementById("setting_container").style.display = "none"
    document.getElementById("wordset_container").style.display = "block"

    // shuffle array
    shuffleArray(testset)

    // Set time limit
    time_limit = document.getElementById('time_limit').value || time_limit

    // run test on words
    for (let j=0; j<testset.length; j++){
        currentWord = testset[j].id
        await testWord(testset[j].id,time_limit*1000)
    }

    //show result only when test is done
    if(testset[testset.length-1].result != "pending"){
        showResult()
    }
})