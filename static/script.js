function submitForm(){
  let name = document.getElementById("Name").value;
  let email =document.getElementById("Email").value;

  if (name && email){
    alert("Thank you for submitting! A doctor will get back to you shortly");
  }
}
