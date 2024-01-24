

let btnClear = document.getElementById('button-ref')
let inputs = document.querySelectorAll('input')

btnClear.addEventListenerbtnClear('click', ()=>
{

var word = "Hello, World!";
console.log(word);
/*above 2 line added for tesing purpose*/
inputs.forEach(input=> input.value = '');
})