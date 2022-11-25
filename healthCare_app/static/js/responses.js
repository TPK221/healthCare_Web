function getBotResponse(input) {

    // Simple responses
    if (input == "hello") {
      return "Hello there! How can we help you? <br> 1. How can I make an appointment? <br> 2. How do I register for an account? <br> 3. How can I contact the medical centre? <br><br> <b>Enter a number from the options above.<b>";
    } else if (input == "goodbye") {
      return "Thank you for visiting TYK Medical Centre's Website!";
    } else if (input == "hi") {
      return "Hello there! How can we help you? <br> 1. How can I make an appointment? <br> 2. How do I register for an account? <br> 3. How can I contact the medical centre? <br><br> <b>Enter a number from the options above.<b>";
    } else if (input == "bye") {
      return "Thank you for visiting TYK Medical Centre's Website!";
    } else if (input == "1") {
      return "You can make an appointment from our Home Page or from the Find A Doctor tab.";
    } else if (input == "2") {
      return "You can register for an account by clicking on the Log In/Register button on the top right and key in your personal details.";
    } else if (input == "3") {
          return "You can contact us via WhatsApp by clicking on the Contact Us button on the top right.";
    } else {
      return "Try to enter another message!";
    }
  
  
  
  }
  