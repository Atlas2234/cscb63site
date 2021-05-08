/*
smooth scrolling
*/

//select link class
const scrollLinks = document.querySelectorAll(".scroll-link");
scrollLinks.forEach(link => {
 link.addEventListener("click", e => {
  e.preventDefault();

  const element = document.getElementById("title");

  let position = element.offsetTop - 658.69;

  window.scrollTo({
   left: 0,
   top: position,
   behavior: "smooth"
  });
 });
});