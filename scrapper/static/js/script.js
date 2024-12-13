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
  document.querySelector(".data-container").style.display = "none";
  const loadingBarContainer = document.getElementById("loading-bar-container");
  const loadingBarFill = document.querySelector(".loading-bar-fill");
  loadingBarContainer.style.display = "block";
  const resultsContainer = document.getElementById("results");

  // Collect input field values
  const origin = document.getElementById("origin").value;
  const destination = document.getElementById("destination").value;
  const departure_date = document.getElementById("departure-date").value;

  fetch('/start_task', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      origin: origin,
      destination: destination,
      departure_date: departure_date,
    }),
  })
    .then(response => response.json())
    .then(() => {
      const interval = setInterval(() => {
        // Fetch progress bar from server
        fetch('/get_progress')
          .then(response => response.json())
          .then(data => {
            const progress = data.progress;
            loadingBarFill.style.width = `${progress}%`;
            if (progress >=100) {
              pollForSolution();
              clearInterval(interval);
              
            }
          })
          .catch(error => {
            console.error("error fetching progress: ",error);
            clearInterval(interval);
          });
      }, 1000);
    })    
    .catch(error => {
      console.error("Error starting task:", error);
    });


    function pollForSolution() {
      const solutionInterval = setInterval(() => {
        
        fetch('/get_solution')
          .then(response => response.json())
          .then(data => {
            const solution = data.solution;
            
            if (solution !== -1) {
              clearInterval(solutionInterval);  
              setTimeout(() => {
                loadingBarContainer.style.display = "none";
                resultsContainer.style.display = "block";
                resultsContainer.textContent = `Your flight ticket for ${departure_date} will be ${solution} RON`;
              }, 500); 
            }
          })
          .catch(error => {
            console.error("Error fetching solution:", error);
            clearInterval(solutionInterval);  
          });
      }, 1000);  
    }
  }

