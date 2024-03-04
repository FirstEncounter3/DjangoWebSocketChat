const passInput = document.getElementById("id_password")
const usernameInput = document.getElementById("id_username")

passInput.placeholder = 'password'
usernameInput.placeholder = 'username'

passInput.classList.add("textInput")

document.querySelector("label[for='id_username']").remove()
document.querySelector("label[for='id_password']").remove()