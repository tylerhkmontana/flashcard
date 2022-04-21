const num_words = document.getElementById('num_words')
const wordset_container = document.getElementById('wordset_container')
let curr_num = num_words.value

num_words.addEventListener('change', (e) => {
    let num = e.target.value
    
    if(curr_num < num) {
        const input_name = document.createElement('input')
        const input_description = document.createElement('input')
        const word_container = document.createElement('div')
        word_container.setAttribute('class', 'word_container')
        input_name.setAttribute('name', 'word')
        input_name.setAttribute('placeholder', 'word')
        input_description.setAttribute('name', 'description')
        input_description.setAttribute('placeholder', 'description')
        word_container.appendChild(input_name)
        word_container.appendChild(input_description)
        wordset_container.appendChild(word_container)
    } else if (curr_num > num) {
        wordset_container.removeChild(wordset_container.lastChild)
    }

    curr_num = num
})