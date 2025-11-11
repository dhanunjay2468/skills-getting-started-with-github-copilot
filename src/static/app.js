document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message / previous items
      activitiesList.innerHTML = "";

      // Reset activity select (keep default placeholder)
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // Basic content (participants appended below)
        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        `;

        // Build participants section using DOM (safe, flexible)
        const participantsWrap = document.createElement("div");
        participantsWrap.className = "participants";

        const participantsHeader = document.createElement("p");
        participantsHeader.className = "participants-header";
        participantsHeader.innerHTML = "<strong>Participants:</strong>";
        participantsWrap.appendChild(participantsHeader);

        if (Array.isArray(details.participants) && details.participants.length > 0) {
          const ul = document.createElement("ul");
          ul.className = "participants-list";

          details.participants.forEach((participant) => {
            const li = document.createElement("li");
            li.className = "participant-item";

            // Name container
            const nameSpan = document.createElement("span");
            nameSpan.textContent = participant; // safe text insertion

            // Delete button (unregister)
            const deleteBtn = document.createElement("button");
            deleteBtn.type = "button";
            deleteBtn.className = "delete-btn";
            deleteBtn.title = "Unregister participant";
            deleteBtn.innerHTML = "&times;"; // simple × icon

            // Wire up unregister action
            deleteBtn.addEventListener("click", async (e) => {
              e.stopPropagation();
              // Call server to unregister and refresh the list on success
              try {
                const resp = await fetch(
                  `/activities/${encodeURIComponent(name)}/unregister?email=${encodeURIComponent(participant)}`,
                  { method: "POST" }
                );

                const result = await resp.json();

                if (resp.ok) {
                  // Refresh activities to reflect change
                  fetchActivities();
                  messageDiv.textContent = result.message || "Participant unregistered";
                  messageDiv.className = "success";
                  messageDiv.classList.remove("hidden");
                  setTimeout(() => messageDiv.classList.add("hidden"), 3000);
                } else {
                  messageDiv.textContent = result.detail || result.message || "Failed to unregister";
                  messageDiv.className = "error";
                  messageDiv.classList.remove("hidden");
                }
              } catch (err) {
                console.error("Error unregistering participant:", err);
                messageDiv.textContent = "Failed to unregister. Please try again.";
                messageDiv.className = "error";
                messageDiv.classList.remove("hidden");
              }
            });

            li.appendChild(nameSpan);
            li.appendChild(deleteBtn);
            ul.appendChild(li);
          });

          participantsWrap.appendChild(ul);
        } else {
          const none = document.createElement("p");
          none.className = "no-participants";
          none.textContent = "No participants yet — be the first!";
          participantsWrap.appendChild(none);
        }

        activityCard.appendChild(participantsWrap);
        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        // Refresh the activities list so the newly registered participant appears
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
