//array of job list. naturally would need more jobs and use better key words.
let jobs = [
    "Software Engineer", "Data Scientist", "Researcher", "Web Developer", 
    "UI/UX Designer", "Teacher", "Full Stack Developer", "Mobile Developer", "Cybersecurity"
];

// function to make drop down box have jobs to choose from (i.e populate scroller)
function populateJobDropdownBox() {
    const selectElement = document.getElementById('job-select');

    // loop through the jobs array
    jobs.forEach(function(job) {
        let option = document.createElement('option'); // option cuz it looks like an option

        // when a value is referrenced in future it will be like software-engineer
        option.value = job.toLowerCase().replace(/\s+/g, '-');

        option.text = job;  // Set the display text
        selectElement.appendChild(option);  // Add the option to the dropdown
    });
}

// Function to handle when user selects a job
function handleJobSelection(event) {
    const selectedJob = event.target.value;  // get the value of the selected job
    console.log("Selected job:", selectedJob);  // we check if this works if the console prints the selected job
    
    //todo get data from this selected job and show statistics based on it

}

// populate dropdown when page loads
window.onload = function() {
    populateJobDropdownBox();

    // get the html element job select
    const selectElement = document.getElementById('job-select');
    selectElement.addEventListener('change', handleJobSelection);  // when user clicks, a change is recorded and 
                                                                   // handleJobSelection function is called

};