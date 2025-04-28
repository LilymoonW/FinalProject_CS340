const story = [
    "You wake up to the soft rustling of leaves above you. A mysterious forest surrounds you.",
    "A worn path stretches into the distance. You start walking, unsure of where it leads.",
    "You find a strange glowing object on the ground. It pulses with light as you touch it.",
    "Suddenly, everything fades to white. A voice echoes: 'Welcome, traveler...'",
    "To be continued..."
  ];
  
  let currentIndex = 0;
  
  function showPage(index) {
    const storyDiv = document.getElementById("story");
    storyDiv.textContent = story[index];
  }
  
  document.getElementById("nextBtn").addEventListener("click", () => {
    currentIndex++;
    if (currentIndex < story.length) {
      showPage(currentIndex);
    } else {
      document.getElementById("story").textContent = "The story ends here... for now.";
      document.getElementById("nextBtn").disabled = true;
    }
  });
  
  window.onload = () => {
    showPage(currentIndex);
  };
  