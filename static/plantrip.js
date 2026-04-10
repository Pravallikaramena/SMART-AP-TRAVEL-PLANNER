function detectLocation() {
    if (!navigator.geolocation) {
        alert("Geolocation not supported in this browser");
        return;
    }

    navigator.geolocation.getCurrentPosition(function(position) {
        let lat = position.coords.latitude;
        let lon = position.coords.longitude;
        console.log("Latitude:", lat, "Longitude:", lon);

        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&accept-language=en`)
            .then(res => res.json())
            .then(data => {
                console.log("Location Data:", data);
                let addr = data.address;
                let city = addr.city || addr.town || addr.municipality || addr.county || "";
                
                let area = addr.amenity || addr.building || addr.highway || addr.historic || 
                           addr.leisure || addr.man_made || addr.shop || addr.tourism || 
                           addr.house_number || addr.road || addr.suburb || addr.neighbourhood || 
                           addr.quarter || addr.residential || addr.village || addr.hamlet || 
                           addr.city_district || "";

                if (!area && data.display_name) {
                    area = data.display_name.split(",")[0];
                }

                if (area && addr.road && area !== addr.road) {
                    area = area + ", " + addr.road;
                }

                if (area && city && area.toLowerCase() === city.toLowerCase()) {
                    area = "";
                }

                let areaDisplay = city;
                if (area && city) areaDisplay = area + ", " + city;
                else if (area) areaDisplay = area;

                document.getElementById("currentArea").value = areaDisplay;

                let citySelect = document.querySelector('input[name="location"]');
                let cityMap = {
                    "Visakhapatnam": "Vizag",
                    "Rajamahendravaram": "Rajahmundry",
                    "Rajahmundry": "Rajahmundry",
                    "Vijayawada": "Vijayawada",
                    "Tirupati": "Tirupati",
                    "Kakinada": "Kakinada"
                };

                if (cityMap[city]) {
                    citySelect.value = cityMap[city];
                } else if (city) {
                    citySelect.value = city;
                }
            })
            .catch(error => {
                console.error("Reverse geocoding error:", error);
                alert("Unable to detect area. Please try again.");
            });
    }, function(error) {
        console.error("Geolocation error:", error);
        alert("Location access denied or timed out. Please allow location permission.");
    }, {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 0
    });
}

function showMessage(msg, isError = true) {
    const alertBox = document.getElementById("alertBox");
    if (!alertBox) {
        alert(msg); // Fallback
        return;
    }
    alertBox.innerText = msg;
    alertBox.style.display = "block";
    alertBox.style.backgroundColor = isError ? "#ffe6e6" : "#e6ffec";
    alertBox.style.color = isError ? "#cc0000" : "#008037";
    alertBox.style.borderColor = isError ? "#ff9999" : "#a8f0ba";
    
    // Scroll to top to see error
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function checkBudget() {
    console.log("Budget check started...");
    
    // Reset alert box
    const alertBox = document.getElementById("alertBox");
    if (alertBox) alertBox.style.display = "none";

    const form = document.getElementById("tripPlannerForm");
    if (!form) {
        console.error("Form #tripPlannerForm not found");
        return false;
    }

    const location = (form.querySelector('input[name="location"]') || {}).value;
    const destination = (form.querySelector('input[name="destination"]') || {}).value;
    const budget = (document.getElementById("budgetInput") || {}).value;
    const days = (form.querySelector('input[name="days"]') || {}).value || 1;
    const travelType = (form.querySelector('select[name="travel_type"]') || {}).value;

    console.log("Inputs:", { location, destination, budget, days, travelType });

    if (!location) {
        showMessage("Please search and select your Current City.");
        return false;
    }
    if (!destination) {
        showMessage("Please search and select your Destination City.");
        return false;
    }
    if (!travelType) {
        showMessage("Please select a Travel Type (Bike, Car, Train, Bus, or Auto).");
        return false;
    }
    if (!budget) {
        showMessage("Please enter your travel budget.");
        return false;
    }

    if (parseInt(budget) < 500) {
        showMessage("Minimum travel budget should be ₹500");
        return false;
    }

    const submitBtn = form.querySelector('button[onclick="checkBudget()"]');
    if (!submitBtn) {
        console.error("Submit button not found");
        return false;
    }

    const originalText = submitBtn.innerText;
    submitBtn.innerText = "Checking...";
    submitBtn.disabled = true;

    try {
        console.log("Calling /validate_trip...");
        const response = await fetch('/validate_trip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: location,
                destination: destination,
                budget: budget,
                days: days,
                travel_type: travelType
            })
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(`Server Issue (${response.status})`);
        }

        const result = await response.json();
        console.log("Validation result:", result);

        if (!result.valid) {
            showMessage(result.message || "Budget validation failed.");
            submitBtn.innerText = originalText;
            submitBtn.disabled = false;
            return false;
        }

        console.log("Validation success! Submitting form...");
        submitBtn.innerText = "Success! Redirecting...";
        form.submit();
        return true;

    } catch (error) {
        console.error("Critical Failure:", error);
        showMessage("Error: " + error.message);
        submitBtn.innerText = originalText;
        submitBtn.disabled = false;
        return false;
    }
}
