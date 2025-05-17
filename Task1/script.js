let expenses = [];

function addExpense() {
    const categoryInput = document.getElementById('category');
    const amountInput = document.getElementById('amount');
    
    const category = categoryInput.value.trim();
    const amount = parseFloat(amountInput.value);
    
    if (category && !isNaN(amount) && amount > 0) {
        expenses.push({ category, amount });
        updateExpensesTable();
        clearInputs();
    } else {
        alert('Please enter correct data');
    }
}

function clearInputs() {
    document.getElementById('category').value = '';
    document.getElementById('amount').value = '';
}

function updateExpensesTable() {
    const tbody = document.getElementById('expensesList');
    tbody.innerHTML = '';
    
    expenses.forEach((expense, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${expense.category}</td>
            <td>${expense.amount.toLocaleString()} $</td>
            <td>
                <button class="delete-btn" onclick="deleteExpense(${index})">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function deleteExpense(index) {
    expenses.splice(index, 1);
    updateExpensesTable();
}

function calculateResults() {
    if (expenses.length === 0) {
        alert('Add at least one expense');
        return;
    }

    const totalAmount = expenses.reduce((sum, expense) => sum + expense.amount, 0);
 
    const averageDaily = totalAmount / 30;

    const topExpenses = [...expenses]
        .sort((a, b) => b.amount - a.amount)
        .slice(0, 3);

    document.getElementById('totalAmount').textContent = `${totalAmount.toLocaleString()} $`;
    document.getElementById('averageDaily').textContent = `${averageDaily.toLocaleString()} $`;
    
    const topExpensesList = document.getElementById('topExpenses');
    topExpensesList.innerHTML = '';
    topExpenses.forEach(expense => {
        const li = document.createElement('li');
        li.textContent = `${expense.category}: ${expense.amount.toLocaleString()} $`;
        topExpensesList.appendChild(li);
    });
} 