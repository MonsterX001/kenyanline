
$(document).ready(function() {
  $('#comment-form').submit(function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the form data
    var formData = $(this).serialize();

    // Send an AJAX request to the server
    $.ajax({
      url: '',  // Replace with the URL to your Django view for handling the comment submission
      type: 'POST',
      data: formData,
      success: function(response) {
        // Handle the response from the server
        if (response.success) {
          // Clear the form
          $('#comment-form textarea').val('');
          // Append the new comment to the comments section
          var newComment = '<p>' + response.comment_text + '</p>';
          $('#comments-section').append(newComment);
          alert('Comment posted successfully!');
        } else {
          alert('Failed to post comment: ' + response.error);
        }
      },
      error: function() {
        alert('An error occurred while posting the comment.');
      }
    });
  });
});

