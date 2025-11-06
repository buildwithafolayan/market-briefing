<script>
  // --- Market Briefing Demo Script ---

  // 1. Get all the HTML elements we need to work with
  const briefingForm = document.getElementById('briefing-form');
  const emailInput = document.getElementById('briefing-email');
  const submitButton = document.getElementById('briefing-submit');
  const messageElement = document.getElementById('briefing-message');

  // 2. !! IMPORTANT: This is your API's URL !!
  //    Replace this with your Vercel URL
  const apiUrl = 'https://market-briefing.vercel.app/api/app';

  // 3. Listen for when the user clicks the "submit" button
  briefingForm.addEventListener('submit', async (event) => {
    // This stops the page from reloading, which is the default
    event.preventDefault();

    // Give the user feedback
    submitButton.textContent = 'Sending...';
    submitButton.disabled = true;
    messageElement.textContent = ''; // Clear any old messages

    // Get the email the user typed in
    const userEmail = emailInput.value;

    try {
      // 4. Send the user's email to our Python API
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // This is the data our Python script expects:
        body: JSON.stringify({ email: userEmail }),
      });

      // 5. Check if the Python script was successful
      if (response.ok) {
        // It worked! Show a success message.
        messageElement.textContent = 'Success! Check your inbox for the report.';
        messageElement.style.color = 'green';
        emailInput.value = ''; // Clear the input field
      } else {
        // The script sent back an error (like "Invalid email")
        const errorData = await response.json();
        messageElement.textContent = `Error: ${errorData.error}`;
        messageElement.style.color = 'red';
      }

    } catch (error) {
      // This catches network errors (e.g., internet is down)
      console.error('Fetch Error:', error);
      messageElement.textContent = 'A network error occurred. Please try again.';
      messageElement.style.color = 'red';
    }

    // 6. Re-enable the button
    submitButton.textContent = 'Send Report';
    submitButton.disabled = false;
  });
</script>