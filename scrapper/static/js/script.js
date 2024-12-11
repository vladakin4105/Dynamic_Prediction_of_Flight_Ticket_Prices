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

//contact form function
function sendMail() {
  // Preia valorile introduse de utilizator
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const contactNo = document.getElementById("contact_no").value.trim();
  const message = document.getElementById("message").value.trim();

  // Construiește URL-ul mailto
  const subject = `Contact Form Submission from ${name}`;
  const body = `Name: ${name}%0D%0AEmail: ${email}%0D%0AContact No: ${contactNo}%0D%0AMessage: ${message}`;
  const mailtoLink = `mailto:youremail@example.com?subject=${encodeURIComponent(
    subject
  )}&body=${encodeURIComponent(body)}`;

  // Redirecționează către link-ul mailto
  window.location.href = mailtoLink;
}

function showLoadingBar(event) {
  event.preventDefault(); // Prevent form submission for demo purposes
  document.querySelector(".formular").style.display = "none";
  const loadingBarContainer = document.getElementById("loading-bar-container");
  const loadingPercentage = document.getElementById("loading-percentage");
  loadingBarContainer.style.display = "block";

  let progress = 0;
  const interval = setInterval(() => {
    if (progress >= 100) {
      clearInterval(interval);
      loadingPercentage.textContent = "Completed!";
      // Simulate actual form submission or next steps
      setTimeout(() => {
        console.log("Form processing complete.");
      }, 500);
    } else {
      progress += 1;
      loadingPercentage.textContent = `${progress}%`;
    }
  }, 20);
}
