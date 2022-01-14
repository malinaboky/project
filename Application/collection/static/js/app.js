const handleEditClickOne = () => {
  document.querySelector("#junior_group").classList.toggle("hide");
  console.log('ppp');
}

const handleEditClickTwo = () => {
  document.querySelector("#middle_group").classList.toggle("hide");
  console.log('ppp');
}

const handleEditClickThree = () => {
  document.querySelector("#senior_group").classList.toggle("hide");
  console.log('ppp');
}

const handleEditClickFour = () => {
  document.querySelector("#preparatory_group").classList.toggle("hide");
  console.log('ppp');
}

document.querySelector("#bt-junior_group").addEventListener("click", handleEditClickOne);
document.querySelector("#bt-middle_group").addEventListener("click", handleEditClickTwo);
document.querySelector("#bt-senior_group").addEventListener("click", handleEditClickThree);
document.querySelector("#bt-preparatory_group").addEventListener("click", handleEditClickFour);
