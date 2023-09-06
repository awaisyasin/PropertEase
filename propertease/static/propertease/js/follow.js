function showAlert(message) {
	var alertBox = document.getElementById('alert');
	alertBox.querySelector('.message').textContent = message;
	alertBox.classList.add('show');
}

function closeAlert() {
	var alertBox = document.getElementById('alert');
	alertBox.classList.remove('show');
}

$(document).ready(function() {
	$('.follow-button').click(function(event) {
	event.preventDefault();

	var followerId = $(this).data('follower-id');
	var followeeId = $(this).data('followee-id');

	// Send AJAX POST request to follow_user_view
	$.ajax({
		url: '/follow/' + followerId + '/' + followeeId + '/',
		method: 'POST',
		headers: {
		'X-CSRFToken': csrfToken
		},
		success: function(response) {
		// Handle success response
		console.log(response);
		// Update UI, show success message, etc.
		showAlert('Successfully followed the user.');
		setTimeout(function() {
			location.reload()
		}, 2000)
		},
		error: function(xhr, status, error) {
		// Handle error response
		console.error(xhr.responseText);
		// Show error message, handle errors, etc.
		showAlert('An error occurred. Please try again later.');
		}
	});
	});
});