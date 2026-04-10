document.addEventListener("DOMContentLoaded", function () {

if (typeof rf === "undefined") return;

const ctx = document.getElementById("accuracyChart").getContext("2d");

new Chart(ctx, {

type: "bar",

data: {

labels: ["Random Forest", "KNN"],

datasets: [{
label: "Accuracy (%)",
data: [rf, knn],

backgroundColor: [
"#2ecc71",
"#1a73e8"
],

borderRadius: 100

}]

},

options: {

responsive: true,

plugins: {

legend: {
labels: {
font: {
size: 100,
weight: "bold"
}
}
},

tooltip: {
titleFont: {
size: 18
},
bodyFont: {
size: 18
}
}

},

scales: {

x: {

ticks: {
font: {
size: 22,
weight: "bold"
}
}

},

y: {

beginAtZero: true,
max: 100,

ticks: {
font: {
size: 30,
weight: "bold"
}
}

}

}

}

});

});