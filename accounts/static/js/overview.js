var mobileNavOpen = false;
var week_profile_visits_data = $('#profileWeekData').text();
week_profile_visits_data = JSON.parse(week_profile_visits_data);


const weeklyChart = new Chart("weeklyChart", {
    type: "line",
    data: {
        labels: ["4 Weeks Ago", "3 Weeks Ago", "2 Weeks Ago", "Past Week"],
        datasets: [{
            label: "Profile Visits",
            data: week_profile_visits_data,
            borderColor: "#022140",
            fill: false,
            tension: 0.3
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                ticks: {
                    beginAtZero: true,
                    stepSize: 1  // Set stepSize to 1 to force whole numbers only
                }
            }
        }
    }
});

$('#mobileNavOpenButton').click(function(event) {
    event.stopPropagation(); // Stop event propagation
    openSideNavbar();
    mobileNavOpen = true;
    //console.log("mobileNavOpen: " + mobileNavOpen);
});

$(document).on('click', function(event) {
    if (!$(event.target).closest('#sideNavbar').length && !$(event.target).is('#mobileNavOpenButton') && mobileNavOpen) {
        closeSideNavbar();
        mobileNavOpen = false;
        //console.log("mobileNavOpen: " + mobileNavOpen);
    }
});

