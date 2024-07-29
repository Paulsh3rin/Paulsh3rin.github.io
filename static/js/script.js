document.getElementById('contact-form').addEventListener('submit', function(event) {
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

// New code for date filters, income, expense, and chart rendering
document.addEventListener('DOMContentLoaded', function() {
    // Check if we are on the dashboard page
    if (document.getElementById('filterButton')) {
        // Event listener for the filter button
        document.getElementById('filterButton').addEventListener('click', fetchDataAndRenderChart);
    }
});

function fetchDataAndRenderChart() {
    const fromDate = document.getElementById('fromDate').value;
    const toDate = document.getElementById('toDate').value;

    fetch(`/api/data?fromDate=${fromDate}&toDate=${toDate}`)
        .then(response => response.json())
        .then(data => {
            // Update income and expense
            updateIncomeAndExpense(data);

            // Render the chart
            renderChart(data.transactions);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function updateIncomeAndExpense(data) {
    const incomeElement = document.getElementById('income');
    const expenseElement = document.getElementById('expense');

    incomeElement.textContent = data.income.toFixed(2); // Ensure toFixed(2) for formatting
    expenseElement.textContent = data.expense.toFixed(2); // Ensure toFixed(2) for formatting
}

function renderChart(data) {
    const labels = data.map(item => item.Date);
    const debitData = data.map(item => item.Debit);

    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
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