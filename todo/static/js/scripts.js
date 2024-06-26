function showTaskDetail(taskId) {
    fetch(`/task/${taskId}/detail/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch task details.');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('taskDetailTitle').innerText = `Title: ${data.title}`;
            document.getElementById('taskDetailDueDate').innerText = `Due Date: ${data.due_date ? data.due_date : 'No due date set'}`;
            document.getElementById('taskDetailDescription').innerText = `Details: ${data.details ? data.details : 'No details available'}`;
            $('#taskDetailModal').modal('show');
        })
        .catch(error => console.error('Error fetching or displaying task details:', error));
}

function toggleTask(taskId) {
    fetch(`/toggle-task/${taskId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ completed: event.target.checked })
    }).then(response => {
        if (!response.ok) {
            alert('Failed to update task.');
        } else {
            location.reload();
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}