function showSidebar() {
  const sideBar = document.querySelector(".sidebar");
  sideBar.style.display = "flex";
}

function closeSidebar() {
  const sideBar = document.querySelector(".sidebar");
  sideBar.style.display = "none";
}

//the input date must be at least today's date
const today = new Date().toISOString().split("T")[0];
document.getElementById("departure-date").setAttribute("min", today);
