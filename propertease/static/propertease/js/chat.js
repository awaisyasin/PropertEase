$(document).ready(function() {
	$('#chat-button').click(function() {
	var loggedInUser = $(this).data('username');
	var personToContact = $(this).data('person-to-contact');
	var profileId = $(this).data('profile-id');

	$.ajax({
		url: '/' + profileId + '/chat-endpoint/',
		method: 'POST',
		headers: {
		  'X-CSRFToken': csrfToken
		},
		data: {
		logged_in_user: loggedInUser,
		person_to_contact: personToContact
		},
		success: function(response) {
		// Handle the success response from the server
		console.log(response);

		// Redirect to the chat page using JavaScript
		window.location.href = '/' + profileId + '/chat/?logged_in_user=' + encodeURIComponent(loggedInUser) + '&person_to_contact=' + encodeURIComponent(personToContact);
		},
		error: function(xhr, status, error) {
		// Handle the error response from the server
		console.error(error);
		}
	});
	});
});