function initCharts(rf, dt, knn, labels, precision, recall, support) {
    if (!document.getElementById('compChart')) return;

    // 1. Accuracy Comparison (Bar Chart)
    new Chart(document.getElementById('compChart'), {
        type: 'bar',
        data: {
            labels: ['Random Forest', 'Decision Tree', 'KNN'],
            datasets: [{
                label: 'Accuracy %',
                data: [rf, dt, knn],
                backgroundColor: ['#28a745', '#0077b6', '#ffc107']
            }]
        },
        options: { responsive: true, plugins: { legend: { display: false } } }
    });

    // 2. Support (Top Predicted Places - Horizontal Bar)
    new Chart(document.getElementById('supportChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Support (Data Count)',
                data: support,
                backgroundColor: '#a29bfe'
            }]
        },
        options: { indexAxis: 'y', responsive: true }
    });

    // 3. Precision (Pie Chart)
    new Chart(document.getElementById('precisionChart'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: precision,
                backgroundColor: [
                    '#ff7675', '#74b9ff', '#fab1a0', '#55efc4', '#a29bfe', 
                    '#ffeaa7', '#fd79a8', '#dfe6e9', '#00b894', '#0984e3'
                ]
            }]
        },
        options: { responsive: true }
    });

    // 4. Recall (Bar Chart)
    new Chart(document.getElementById('recallChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Recall %',
                data: recall,
                backgroundColor: '#ff7675'
            }]
        },
        options: { responsive: true }
    });
}
document.addEventListener("DOMContentLoaded", function(){

const trainForm = document.getElementById("trainForm");

if(trainForm){

trainForm.addEventListener("submit", function(e){

e.preventDefault();

/* show pipeline */
document.getElementById("pipelineBox").style.display="block";

/* stages animation */
const stages = ["p2","p3","p4","p5"];

let delay = 0;

stages.forEach((stage)=>{

setTimeout(()=>{

document.getElementById(stage).classList.add("active");

}, delay);

delay += 1200;

});

    /* start loader, send training request and handle result */
    fetch("/train_model", {
        method: "POST"
    }).then(response => {
        if (response.ok) {
            /* Training complete, show success boxes */
            document.querySelector(".loader2").style.display="none";
            document.getElementById("successBox").style.display="flex";
            document.getElementById("pipelineBox").querySelector("h3").textContent = "Training Completed! ✅";
            
            // Mark all stages as active immediately on success
            stages.forEach(s => document.getElementById(s).classList.add("active"));
        } else {
            response.text().then(text => {
                alert("Training failed: " + text);
                document.getElementById("pipelineBox").style.display="none";
                document.querySelector(".loader2").style.display="block";
            });
        }
    }).catch(err => {
        console.error("Training failed:", err);
        alert("Training failed: " + err);
        document.getElementById("pipelineBox").style.display="none";
    });

});

}

});
document.addEventListener("DOMContentLoaded", function(){

const fileInput = document.getElementById("datasetFile");
const fileName = document.getElementById("fileName");

if(fileInput){
fileInput.addEventListener("change", function(){

if(fileInput.files.length > 0){
fileName.textContent = fileInput.files[0].name;
}

});
}

});