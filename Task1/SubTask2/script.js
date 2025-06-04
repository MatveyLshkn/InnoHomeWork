async function runTests() {
    try {
        const response = await fetch('https://fakestoreapi.com/products');
        const products = await response.json();
        
        validateServerResponse(response);
   
        validateProducts(products);
    } catch (error) {
        console.error('Error running tests:', error);
        updateServerResponse({
            status: 0,
            statusText: 'Error: ' + error.message
        });
    }
}

function validateServerResponse(response) {
    const status = response.status;
    const statusText = response.statusText;
    
    updateServerResponse({
        status,
        statusText,
        isSuccess: status === 200
    });
}

function updateServerResponse({ status, statusText, isSuccess }) {
    const statusCodeElement = document.getElementById('statusCode');
    const statusTextElement = document.getElementById('statusText');
    
    statusCodeElement.textContent = status;
    statusTextElement.textContent = statusText;
    
    statusCodeElement.className = isSuccess ? 'status-success' : 'status-error';
    statusTextElement.className = isSuccess ? 'status-success' : 'status-error';
}

function validateProducts(products) {
    const issues = [];
    
    products.forEach((product, index) => {
        const productIssues = [];
        
        if (!product.title || product.title.trim() === '') {
            productIssues.push('Title is empty');
        }
        
        if (typeof product.price !== 'number' || product.price < 0) {
            productIssues.push('Price is invalid or negative');
        }
        
        if (!product.rating || typeof product.rating.rate !== 'number' || product.rating.rate > 5) {
            productIssues.push('Rating rate is invalid or exceeds 5');
        }
        
        if (productIssues.length > 0) {
            issues.push({
                id: product.id,
                title: product.title,
                issues: productIssues
            });
        }
    });
    
    updateValidationResults(products.length, issues);
}

function updateValidationResults(totalProducts, issues) {
    document.getElementById('totalProducts').textContent = totalProducts;
    document.getElementById('productsWithIssues').textContent = issues.length;
    
    const issuesListElement = document.getElementById('issuesList');
    issuesListElement.innerHTML = '';
    
    if (issues.length === 0) {
        issuesListElement.innerHTML = '<p class="status-success">No issues found!</p>';
        return;
    }
    
    issues.forEach(issue => {
        const issueElement = document.createElement('div');
        issueElement.className = 'issue-item';
        
        issueElement.innerHTML = `
            <h5>Product ID: ${issue.id}</h5>
            <p>Title: ${issue.title}</p>
            <div class="issue-details">
                <strong>Issues found:</strong>
                <ul>
                    ${issue.issues.map(i => `<li>${i}</li>`).join('')}
                </ul>
            </div>
        `;
        
        issuesListElement.appendChild(issueElement);
    });
} 