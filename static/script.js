document.addEventListener("DOMContentLoaded", async function() {
    const homeLeagueDropdown = document.getElementById('home_league');
    const awayLeagueDropdown = document.getElementById('away_league');
    const homeDropdown = document.getElementById('home');
    const awayDropdown = document.getElementById('away');
    const resultDiv = document.getElementById('result');

    // Load leagues into dropdowns
    async function loadLeagues() {
        const response = await fetch('/leagues');
        const leagues = await response.json();

        leagues.forEach(league => {
            let option1 = document.createElement('option');
            option1.value = league;
            option1.textContent = league;
            homeLeagueDropdown.appendChild(option1);

            let option2 = document.createElement('option');
            option2.value = league;
            option2.textContent = league;
            awayLeagueDropdown.appendChild(option2);
        });
    }

    async function loadTeams(leagueDropdown, teamDropdown) {
        const league = leagueDropdown.value;
        if (!league) return;

        const response = await fetch(`/teams/${league}`);
        const teams = await response.json();

        // Reset previous options
        teamDropdown.innerHTML = '<option value="">Choose Team</option>';
        teams.forEach(team => {
            let option = document.createElement('option');
            option.value = team;
            option.textContent = team;
            teamDropdown.appendChild(option);
        });
    }

    homeLeagueDropdown.addEventListener('change', () => loadTeams(homeLeagueDropdown, homeDropdown));
    awayLeagueDropdown.addEventListener('change', () => loadTeams(awayLeagueDropdown, awayDropdown));

    document.getElementById('predictForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        resultDiv.innerHTML = `<p>Loading prediction...</p>`; // Show loading message

        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                home_league: homeLeagueDropdown.value,
                away_league: awayLeagueDropdown.value,
                home: homeDropdown.value,
                away: awayDropdown.value
            })
        });

        const result = await response.json();

        if (response.ok) {
            resultDiv.innerHTML = ''; // Clear previous results

            // Show main prediction result
            let scoreLine = document.createElement('p');
            scoreLine.innerHTML = `<strong>${result.result}</strong>`;
            resultDiv.appendChild(scoreLine);

            // Function to create a center-outward progress bar
            function createProgressBar(statName, homeValue, awayValue) {
                let statContainer = document.createElement('div');
                statContainer.classList.add('stat-container');

                // Add stat label at the center above the bar
                let statLabel = document.createElement('div');
                statLabel.classList.add('stat-label');
                statLabel.innerHTML = `<strong>${statName}</strong>`;
                statContainer.appendChild(statLabel);

                // Create a wrapper for the bar and values
                let barWrapper = document.createElement('div');
                barWrapper.classList.add('bar-wrapper');

                let homeValueLabel = document.createElement('span');
                homeValueLabel.classList.add('stat-value-left');
                homeValueLabel.innerText = homeValue;

                let awayValueLabel = document.createElement('span');
                awayValueLabel.classList.add('stat-value-right');
                awayValueLabel.innerText = awayValue;

                let bar = document.createElement('div');
                bar.classList.add('stat-bar');

                let homeBar = document.createElement('div');
                homeBar.classList.add('stat-fill', 'stat-home');
                homeBar.style.width = `${(homeValue / (homeValue + awayValue)) * 50}%`;

                let awayBar = document.createElement('div');
                awayBar.classList.add('stat-fill', 'stat-away');
                awayBar.style.width = `${(awayValue / (homeValue + awayValue)) * 50}%`;

                bar.appendChild(homeBar);
                bar.appendChild(awayBar);

                // Append values and bar to wrapper
                barWrapper.appendChild(homeValueLabel);
                barWrapper.appendChild(bar);
                barWrapper.appendChild(awayValueLabel);

                statContainer.appendChild(barWrapper);

                return statContainer;
            }

            // Show all stats
            const statsToShow = [
                "Ball Possession",
                "Goal Attempts",
                "Shots on Goal",
                "Corner Kicks",
                "Free Kicks",
                "Offsides",
                "Yellow Cards"
            ];

            statsToShow.forEach(stat => {
                const values = result.stats[stat].split(" - ");
                const homeValue = parseFloat(values[0].replace("%", "")); // Remove % sign if present
                const awayValue = parseFloat(values[1].replace("%", ""));
                resultDiv.appendChild(createProgressBar(stat, homeValue, awayValue));
            });

            // Show prediction accuracy
            let accuracyLine = document.createElement('p');
            accuracyLine.innerHTML = `<strong>Prediction Accuracy:</strong> ${result.accuracy}`;
            resultDiv.appendChild(accuracyLine);

            // Show reasoning
            let reasonLine = document.createElement('p');
            reasonLine.innerHTML = `<strong>Reason:</strong> ${result.reason}`;
            resultDiv.appendChild(reasonLine);
        } else {
            resultDiv.innerHTML = `<p style="color:red;">${result.error}</p>`;
        }
    });

    loadLeagues();
});
