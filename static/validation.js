// ================= LOGIN VALIDATION =================

function validateLogin(){

let email = document.querySelector('input[name="email"]').value
let password = document.querySelector('input[name="password"]').value

if(email == "" || password == ""){
alert("Please enter email and password")
return false
}

let emailPattern = /^[A-Za-z][A-Za-z0-9._]*@gmail\.com$/;

if(!email.match(emailPattern)){
alert("Enter valid Gmail address")
return false
}

return true
}



// ================= PASSWORD SHOW / HIDE =================

function togglePassword(fieldId, element){

let pass = document.getElementById(fieldId)
let icon = element.querySelector("i")

if(pass.type === "password"){

pass.type = "text"
icon.classList.remove("fa-eye-slash")
icon.classList.add("fa-eye")

}else{

pass.type = "password"
icon.classList.remove("fa-eye")
icon.classList.add("fa-eye-slash")

}

}



// ================= PAGE LOAD EVENTS =================

document.addEventListener("DOMContentLoaded", function(){


// ---------- NAME VALIDATION ----------

let name = document.getElementById("name")
let nameError = document.getElementById("nameError")

if(name){

name.addEventListener("input", function(){

let value = name.value

if(value.length == 0){
nameError.innerHTML = "Name required"
nameError.style.color = "red"
}

else if(!/^[A-Za-z ]+$/.test(value)){
nameError.innerHTML = "Only letters allowed"
nameError.style.color = "red"
}

else{
nameError.innerHTML = ""
}

})

}



// ---------- PHONE VALIDATION ----------

let phone = document.getElementById("phone")
let phoneError = document.getElementById("phoneError")

if(phone){

phone.addEventListener("input", function(){

let value = phone.value

if(value.length == 0){
phoneError.innerHTML = "Phone number required"
phoneError.style.color = "red"
}

else if(/[^0-9]/.test(value)){
phoneError.innerHTML = "Only numbers are allowed"
phoneError.style.color = "red"
}

else if(value.length < 10){
phoneError.innerHTML = "Enter valid 10 digit phone number"
phoneError.style.color = "red"
}

else if(value.length == 10){
phoneError.innerHTML = ""
}

})

}



// ---------- EMAIL VALIDATION ----------

let email = document.getElementById("email")
let emailError = document.getElementById("emailError")

if(email){

email.addEventListener("input", function(){

let value = email.value

if(value.length == 0){
emailError.innerHTML = "Email required"
emailError.style.color = "red"
}

else if(!/^[A-Za-z][A-Za-z0-9._]*@gmail\.com$/.test(value)){
emailError.innerHTML = "Enter valid Gmail address"
emailError.style.color = "red"
}

else{
emailError.innerHTML = ""
}

})

}



// ---------- PASSWORD STRENGTH ----------

let password = document.getElementById("password")

if(password){

password.addEventListener("keyup", function(){

let value = password.value
let bar = document.getElementById("strengthBar")
let text = document.getElementById("strengthText")

if(value.length < 6){

bar.innerHTML = "█░░░░"
text.innerHTML = "Weak"
text.style.color = "red"

}
else if(value.length < 10){

bar.innerHTML = "███░░"
text.innerHTML = "Medium"
text.style.color = "orange"

}
else{

bar.innerHTML = "█████"
text.innerHTML = "Strong"
text.style.color = "green"

}

})

}



// ---------- PASSWORD MATCH REAL TIME ----------

let confirm = document.getElementById("confirm")

if(confirm){

confirm.addEventListener("keyup", function(){

let error = document.getElementById("error")

if(confirm.value !== password.value){
error.innerHTML = "Passwords do not match"
error.style.color = "red"
}
else{
error.innerHTML = "Passwords match"
error.style.color = "green"
}

})

}

})




// ================= REGISTER SUBMIT VALIDATION =================

function validateRegister(){

let name = document.getElementById("name").value
let phone = document.getElementById("phone").value
let email = document.getElementById("email").value
let password = document.getElementById("password").value
let confirm = document.getElementById("confirm").value


if(name == "" || phone == "" || email == "" || password == "" || confirm == ""){
alert("All fields are required")
return false
}

if(!/^[A-Za-z ]+$/.test(name)){
alert("Name must contain only letters")
return false
}

if(!/^[0-9]{10}$/.test(phone)){
alert("Phone number must be 10 digits")
return false
}

if(!/^[A-Za-z][A-Za-z0-9._]*@gmail\.com$/.test(email)){
alert("Gmail address starts with only letters")
return false
}

if(password !== confirm){
alert("Passwords do not match")
return false
}

return true

}




// RESET PASSWORD VALIDATION

function validateReset(){

let email = document.getElementById("resetEmail").value
let password = document.getElementById("resetPassword").value
let confirm = document.getElementById("resetConfirm").value

let emailError = document.getElementById("resetEmailError")
let passwordError = document.getElementById("resetPasswordError")
let confirmError = document.getElementById("resetConfirmError")

emailError.innerHTML = ""
passwordError.innerHTML = ""
confirmError.innerHTML = ""

let valid = true

// EMAIL REQUIRED

if(email == ""){
emailError.innerHTML = "Email required"
emailError.style.color="red"
valid = false
}


// EMAIL FORMAT (must start with letter + gmail)

else if(!/^[A-Za-z][A-Za-z0-9._]*@gmail\.com$/.test(email)){
emailError.innerHTML = "Email must start with letter and be Gmail"
emailError.style.color="red"
valid = false
}



// PASSWORD REQUIRED

if(password == ""){
passwordError.innerHTML = "Password required"
passwordError.style.color="red"
valid = false
}


// PASSWORD LENGTH

else if(password.length < 6){
passwordError.innerHTML = "Password must be at least 6 characters"
passwordError.style.color="red"
valid = false
}



// CONFIRM PASSWORD REQUIRED

if(confirm == ""){
confirmError.innerHTML = "Confirm password required"
confirmError.style.color="red"
valid = false
}



// PASSWORD MATCH

else if(password !== confirm){
confirmError.innerHTML = "Passwords do not match"
confirmError.style.color="red"
valid = false
}

return valid

}