console.log("Script loaded");

let jobSkills = {};  // dictionary of job to skills

// fetch job skills from app.py
function fetchJobSkills() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            jobSkills = data;  // store job skills dictionary
        })
        .catch(error => console.error('Error fetching job skills:', error));
}

// Function to display skills for the searched job
function displaySkills(skills) {
    const skillsContainer = document.getElementById('skills-container');
    skillsContainer.innerHTML = '';  // clear previous skills list

    skills.forEach(skill => {
        const skillItem = document.createElement('li');
        skillItem.textContent = skill;
        skillsContainer.appendChild(skillItem);
    });
}

// job search functionality
function handleJobSearch() {
    const searchInput = document.getElementById('job-search').value.trim();
    const selectedJob = searchInput;  // capture search term as job title

    if (jobSkills[selectedJob]) {
        // display skills for the searched job
        const skills = jobSkills[selectedJob];
        displaySkills(skills);  // display skills below the search bar
    } else {
        alert("Job not found. Please enter a valid job title.");
    }
}

// Function to provide job search suggestions
function jobSearchSuggestions() {
    const searchInput = document.getElementById('job-search').value.trim().toLowerCase();
    const suggestionsContainer = document.querySelector('.job-search-suggestions');

    // Clear previous suggestions
    suggestionsContainer.innerHTML = '';

    // If search input is empty, do nothing
    if (searchInput === '') return;

    // Get all job titles from jobSkills dictionary
    const jobTitles = Object.keys(jobSkills);

    // Find exact matches
    let filteredJobs = jobTitles.filter(job => job.toLowerCase() === searchInput);

    // If no exact matches, find partial matches
    if (filteredJobs.length === 0) {
        filteredJobs = jobTitles.filter(job => job.toLowerCase().includes(searchInput));
    }

    // Display the filtered job suggestions
    if (filteredJobs.length > 0) {
        filteredJobs.forEach(job => {
            const jobTitle = document.createElement('p');
            jobTitle.textContent = job;

            // Add a click event to fill the search input when a suggestion is clicked
            jobTitle.addEventListener('click', () => {
                document.getElementById('job-search').value = job;
                handleJobSearch();
                suggestionsContainer.innerHTML = ''; // Clear suggestions after selection
            });

            suggestionsContainer.appendChild(jobTitle);
        });
    } else {
        // If no suggestions found, show message
        const noResult = document.createElement('p');
        noResult.textContent = 'No matching jobs found.';
        suggestionsContainer.appendChild(noResult);
    }
}    

// Array of job list
let jobs = [
    "Software Engineer", "Data Scientist", "Researcher", "Web Developer", 
    "UI/UX Designer", "Teacher", "Full Stack Developer", "Mobile Developer", "Cybersecurity"
];

// Function to populate the dropdown box with jobs
function populateJobDropdownBox() {
    const selectElement = document.getElementById('job-select');

    jobs.forEach(function(job) {
        let option = document.createElement('option');
        option.value = job.toLowerCase().replace(/\s+/g, '-');
        option.text = job;
        selectElement.appendChild(option);
    });
}

// Function to create or update the pie chart
function createPieChart(data) {
    const ctx = document.getElementById('jobChart').getContext('2d');
    
    // If a previous chart exists, destroy it
    if (window.myPieChart) {
        window.myPieChart.destroy();
    }

    // Create a new pie chart
    window.myPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Category 1', 'Category 2', 'Category 3'],  // Dummy categories
            datasets: [{
                label: 'Job Data',
                data: data,  // Pass the data to the chart
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true
        }
    });
}

// Function to handle when user selects a job
function handleJobSelection(event) {
    const selectedJob = event.target.value;  // Get the selected job value
    console.log("Selected job:", selectedJob);
    
    // Dummy data for the chart based on selected job
    let chartData;
    if (selectedJob === 'software-engineer') {
        chartData = [10, 20, 30];  // Example data for Software Engineer
    } else if (selectedJob === 'data-scientist') {
        chartData = [15, 25, 35];  // Example data for Data Scientist
    } else if (selectedJob === 'researcher') {
        chartData = [5, 10, 15];  // Example data for Researcher
    } else {
        chartData = [12, 19, 24];  // Default dummy data
    }

    // Create or update the pie chart with the selected data
    createPieChart(chartData);
}

// Populate the dropdown when the page loads
window.onload = function() {
    fetchJobSkills();  // Fetch job skills function called
    populateJobDropdownBox();

    // Event listener for the search input field for suggestions
    const searchInput = document.getElementById('job-search');
    searchInput.addEventListener('input', jobSearchSuggestions);
    
    // Get the dropdown element and add event listener
    const selectElement = document.getElementById('job-select');
    selectElement.addEventListener('change', handleJobSelection);

    // event listener for the search button
    document.getElementById('search-button').addEventListener('click', handleJobSearch);
};
