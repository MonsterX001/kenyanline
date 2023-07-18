document.querySelectorAll("#").forEach(anchor => {
    anchor.addEventListener("click", function(e){
      e.preventDefault();
      document.querySelector(this.getAtribute("href")).ScrollIntoView({
        behaviour : "smooth"
      })
    })
  })
  
      var entryTime = new Date();
  
      function calculateTimeSpent() {
        var exitTime = new Date();
        var timeSpent = exitTime - entryTime;
  
        console.log("Time spent on the page (in milliseconds): " + timeSpent);
  
        // Convert milliseconds to seconds, minutes, or hours as needed
        var seconds = Math.floor(timeSpent / 1000);
        console.log("Time spent on the page (in seconds): " + seconds);
  
        var minutes = Math.floor(timeSpent / (1000 * 60));
        console.log("Time spent on the page (in minutes): " + minutes);
  
        var hours = Math.floor(timeSpent / (1000 * 60 * 60));
        console.log("Time spent on the page (in hours): " + hours);
  
        // Send time spent data to the server
        $.ajax({
          url: '/track-time/',
          type: 'POST',
          data: { time_spent: timeSpent },
          success: function (response) {
            console.log('Time spent saved successfully.');
          },
          error: function (xhr, errmsg, err) {
            console.log('Error occurred while saving time spent.');
          }
        });
  
        // Update the entry time for the next page load
        entryTime = exitTime;
      }
  
      window.addEventListener("beforeunload", calculateTimeSpent);
  