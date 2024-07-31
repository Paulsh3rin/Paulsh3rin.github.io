document.addEventListener('DOMContentLoaded', function() {
    // Ensure the contact form exists before adding an event listener
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;

            if (name && email && message) {
                alert('Thank you for your message!');
            } else {
                alert('Please fill out all fields.');
            }
        });
    }

    // Check if we are on the dashboard page
    const filterButton = document.getElementById('filterButton');
    if (filterButton) {
        // Event listener for the filter button
        filterButton.addEventListener('click', fetchDataAndRenderChart);
    }
});

function fetchDataAndRenderChart() {
    const fromDate = document.getElementById('fromDate').value;
    const toDate = document.getElementById('toDate').value;

    console.log(`Fetching data from ${fromDate} to ${toDate}`);

    fetch(`/api/data?fromDate=${fromDate}&toDate=${toDate}`)
        .then(response => {
            console.log('Fetch response:', response);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('API response:', data);

            updateIncomeAndExpense(data);

            renderChart(data.transactions);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function updateIncomeAndExpense(data) {
    const incomeElement = document.getElementById('income');
    const expenseElement = document.getElementById('expense');

    incomeElement.textContent = data.income.toFixed(2);
    expenseElement.textContent = data.expense.toFixed(2);
}

function renderChart(transactions) {
    const labels = transactions.map(item => item.Date); // Ensure 'Date' matches your data's date field
    const debitData = transactions.map(item => item.Debit); // Ensure 'Debit' matches your data's debit field

    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'line', // or 'bar', 'pie', etc.
        data: {
            labels: labels,
            datasets: [{
                label: 'Debit',
                data: debitData,
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
        }
    });
}
