let tutorialStep = 0;
const robot = document.getElementById("ai-robot-container");
const textObj = document.getElementById("robot-text");
const btnObj = document.getElementById("robot-btn");

function getElementCoordinates(hrefToken) {
    const navLinks = document.querySelectorAll('.nav-links a');
    for (let i=0; i < navLinks.length; i++) {
        if (navLinks[i].getAttribute("href").includes(hrefToken)) {
            const rect = navLinks[i].getBoundingClientRect();
            return {
                top: rect.bottom + 20, 
                left: rect.left - 50
            };
        }
    }
    // fallback center
    return { top: 100, left: window.innerWidth / 2 - 150 };
}

function startAITutorial(event) {
    if(event) event.preventDefault();
    tutorialStep = 0;
    
    // Reset positions and animate in
    robot.style.top = "100px";
    robot.style.left = "50%";
    robot.classList.add("active");
    textObj.innerHTML = "Welcome! I'm your Smart Assistant! 🤖<br>I'll guide you through our Smart AP Travel system step-by-step!";
    btnObj.innerText = "Start Tour!";
}

function nextTutorialStep() {
    tutorialStep++;
    
    if (tutorialStep === 1) {
        textObj.innerHTML = "<b>Step 1: Upload Dataset</b> 📂<br>Click here to provide your travel dataset so I can analyze it!";
        let coords = getElementCoordinates("dataset");
        robot.style.top = coords.top + "px";
        robot.style.left = coords.left + "px";
    } 
    else if (tutorialStep === 2) {
        textObj.innerHTML = "<b>Step 2: Train Model</b> 🧠<br>Once uploaded, click Train Model to configure my Neural Networks!";
        let coords = getElementCoordinates("dataset"); // usually on the same dataset page, so stay near it
        robot.style.top = coords.top + "px";
        robot.style.left = (coords.left + 50) + "px"; // nudge slightly
    }
    else if (tutorialStep === 3) {
        textObj.innerHTML = "<b>Step 3: Charts</b> 📊<br>This page shows you exactly how accurate my AI predictions are!";
        let coords = getElementCoordinates("charts");
        robot.style.top = coords.top + "px";
        robot.style.left = coords.left + "px";
    }
    else if (tutorialStep === 4) {
        textObj.innerHTML = "<b>Step 4: Performance Analysis</b> 📈<br>Check this section to see my deep learning model's training performance!";
        let coords = getElementCoordinates("performance_analysis");
        robot.style.top = coords.top + "px";
        robot.style.left = coords.left + "px";
    }
    else if (tutorialStep === 5) {
        textObj.innerHTML = "<b>Step 5: AI Recommendations</b> ✈️<br>Go to the Home Dashboard and hit 'Start Planning' to get my smart itinerary map!";
        let coords = getElementCoordinates("/");
        robot.style.top = coords.top + "px";
        robot.style.left = coords.left + "px";
        btnObj.innerText = "Finish";
    }
    else {
        // Exit Tutorial
        textObj.innerHTML = "Have a great trip! Beep Boop! ✨";
        btnObj.style.display = "none";
        
        // Fly away animation
        robot.style.top = "-200px";
        
        setTimeout(() => {
            robot.classList.remove("active");
            btnObj.style.display = "inline-block";
        }, 1000);
    }
}
