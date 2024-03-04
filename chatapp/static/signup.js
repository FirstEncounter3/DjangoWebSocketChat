const usernameInput = document.getElementById("id_username")
const passInput1 = document.getElementById("id_password1")
const passInput2 = document.getElementById("id_password2")
const usernameHelpText = document.getElementById("id_username_helptext")
const passwordHelpText = document.getElementById("id_password2_helptext")

usernameInput.placeholder = 'username'
passInput1.placeholder = 'password'
passInput2.placeholder = 'retry password'

passInput1.classList.add("textInput")
passInput2.classList.add("textInput")

document.getElementsByTagName('ul')[0].remove()
document.querySelector("label[for='id_username']").remove()
document.querySelector("label[for='id_password1']").remove()
document.querySelector("label[for='id_password2']").remove()
usernameHelpText.remove()
passwordHelpText.remove()