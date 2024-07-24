$(document).ready(function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
    });

})

// analytics.js
function fetchData(userPageUrl, apiUrl) {
    const loadingSpinners = document.getElementById('loadingSpinners');
    const analytics_data = document.getElementById('analyticsData');

    analytics_data.style.display = 'none';

    // Make an AJAX request to the API endpoint after the HTML is loaded
    fetch(`${apiUrl}?user_page_url=${userPageUrl}`)
        .then(response => response.json())
        .then(data => {

            $('.placeholder-cards-container').css('display', 'none');
            $('.three-data-cards-container').css('display', 'flex');

            //console.log('Visited users total:', data.visited_users);
            //console.log('Visited earlier: ', data.visited_users_past);
            //console.log('Visited users top 5:', data.top5_cities_arr);
            //console.log("total time spent: ", data.time_spent_on_page);

            


            // Create a bar chart for visited users
            //createBarChart('visitedUsersChart', 'Visited Users', data.visited_users.map(user => user.name), data.visited_users.map(user => user.visits));

            // Create a pie chart for top 5 cities
            var chartNames = ['top5year','top5month','top5week', 'top5day']
            var noDataIDs = ["noDataYear","noDataMonth","noDataWeek","noDataDay"]
            var totalVisited = ['totalVistedYear', 'totalVistedMonth', 'totalVistedWeek', 'totalVistedDay']
            var totalVisitedPast = ['totalVistedYearPast', 'totalVistedMonthPast', 'totalVistedWeekPast', 'totalVistedDayPast']
            var visitedChange;
            for (var i = 0; i < data.top5_cities_arr.length; i++) {
                if (data.top5_cities_arr[i].length > 0) createPieChart(chartNames[i], 'Top 5 Cities', data.top5_cities_arr[i]);
                else document.getElementById(noDataIDs[i]).style.display = 'block';
                document.getElementById(totalVisited[i]).innerHTML = `${data.visited_users[i]}`;

                visitedChange = Math.round((data.visited_users[i]/data.visited_users_past[i]) * 100);

                if (data.visited_users_past[i] == 0) {
                    document.getElementById(totalVisitedPast[i]).innerHTML = `no data from past period`;
                } else if (visitedChange > 0)  {
                    document.getElementById(totalVisitedPast[i]).innerHTML = `${visitedChange}% increase`;
                    document.getElementById(totalVisitedPast[i]).style.color = '#097969';
                } else if (visitedChange < 0) {
                    document.getElementById(totalVisitedPast[i]).innerHTML = `${visitedChange}% decrease`;
                    document.getElementById(totalVisitedPast[i]).style.color = '#B90E0A';
                } else {
                    document.getElementById(totalVisitedPast[i]).innerHTML = `-% change`;
                }
                
                //console.log(document.getElementById(noDataIDs[i]).style.display == 'block');
            }          

            loadingSpinners.style.setProperty('display', 'none', 'important');
            analytics_data.style.display = 'block';

            $('#avgTimeSpent').text(data.time_spent_on_page + 's');
        })
        .catch(error => console.error('Error:', error));
        
}


function createBarChart(chartId, chartLabel, labels, data) {
    const ctx = document.getElementById(chartId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            //labels: labels,
            datasets: [{
                label: chartLabel,
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    });
}

function createPieChart(chartId, chartLabel, data) {
    //console.log("data:" + data);

    const labels = [];
    const values = [];

    // can be done with nested maps for better performance
    if (data.length > 0) {
        for(var i = 0; i < data.length; i++){
            //console.log(data[i][0]);    //debugigng
            labels.push(data[i][0]);
            values.push(data[i][1]);
        }

        const ctx = document.getElementById(chartId).getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            },
        });
    } 
}
