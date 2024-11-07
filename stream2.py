import streamlit as st
import streamlit.components.v1 as components

html_code = '''

<!DOCTYPE html>
<html lang="en">
  
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>

    *{
      padding: 0;
      margin: 0;
      font-family: 'Poppins', sans-serif;
      box-sizing: border-box;
    }

    .container {
        width: 100%;  
        height: 100%;
        max-width: 1000px; 
        margin: 0 auto;
        }

    body{
      width: 100%;
      height: 100vh;
      background-color: #33343f;
    }

    .chat{
      display: flex;
      gap: 20px;
      padding: 25px;
      color: #fff;
      font-size: 15px;
      font-weight: 300;
    }

    .chat img{
      width: 35px;
      height: 35px;
    }

    .response{
      background-color: #494b59;
    }

    .messagebar{
      position: fixed;
      bottom: 0;
      height: 5rem;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      border-top: 1px solid #494b59;
      background-color: #33343f;
    }

    .messagebar .bar-wrapper{
      background-color: #494b59;
      border-radius: 5px;
      width: 60vw;
      padding: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .bar-wrapper input{
      width: 100%;
      padding: 5px;
      border: none;
      outline: none;
      font-size: 14px;
      background: none;
      color: #ccc;
    }

    .bar-wrapper input::placeholder{
      color: #ccc;
    }

    .messagebar button{
      display: flex;
      align-items: center;
      justify-content: center;
      background: none;
      border: none;
      color: #fff;
      cursor: pointer;
    }

    .message-box{
      height: calc(100vh - 5rem);
      overflow-y: auto;
    }

  </style>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300&display=swap" rel="stylesheet">
  <title>Document</title>

</head>
<body>
  <div class="chatbox-wrapper">
    <div class="message-box">
      <div class="chat response">
        <img src="https://media.licdn.com/dms/image/v2/C510BAQEqZ449wmfp7g/company-logo_200_200/company-logo_200_200/0/1630594009880?e=2147483647&v=beta&t=Nx7_NH__ivA_XUM2CJCyqnisOKTFIIW2ztCIS4KH7jg">
        <span>Hello there! <br> 
          How can I help you today.
        </span>
      </div>
    </div>
    <div class="messagebar">
      <div class="bar-wrapper">
        <input type="text" placeholder="Enter your message...">
        <button>
          <span class="material-symbols-rounded">
            send
            </span>
        </button>
      </div>
    </div>
  </div>

  <script>// Selecting HTML elements
    const messageBar = document.querySelector(".bar-wrapper input");
    const sendBtn = document.querySelector(".bar-wrapper button");
    const messageBox = document.querySelector(".message-box");
    
    
    // API configuration for Groq
    const API_URL = "https://api.groq.com/openai/v1/chat/completions";
    const API_KEY = // Replace with your actual Groq API key
    
    // Hardcoded company information from JSON file
    const companyInfo = {
        "role": "user",
        "content": {
          "Company Name": "RUGVED SYSTEMS INC",
        
          "Full Form": "Remote Unmanned Ground Vehicular Electronics Defence systems",
          "Description": "RUGVED SYSTEMS is a defence related student project from MIT Manipal. They work on different panels like surveillance, law enforcement, military assist, and civil defence. They participate in international competitions like IGVC, etc. They also had a contract with DRDO in building defence related projects.",
          //put in your organisations details here..
        }
    }
    
    // Custom response middleware
    function customResponseMiddleware(response) {
      if (response.includes("Mistral and NVIDIA")) {
        response = response.replace("Mistral and NVIDIA", "RUGVED SYSTEMS Inc");
      }
      return response;
    }
    
    // // Function to generate response using Groq API
    // async function generateResponse(userInput, companyInfo) {
    //   const messages = [
    //     { role: "system", content: `Company Info: ${JSON.stringify(companyInfo)}` },
    //     { role: "user", content: userInput }
    //   ];
    
    //   const requestOptions = {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //       "Authorization": `Bearer ${API_KEY}`
    //     },
    //     body: JSON.stringify({
    //       model: "llama3-8b-8192",  // Replace with the correct Groq model ID
    //       messages: messages,
    //       temperature: 1,
    //       top_p: 1,
    //       stream: false,
    //       stop: null
    //     })
    //   };
    
    //   const response = await fetch(API_URL, requestOptions);
    
    //   if (response.ok) {
    //     const data = await response.json();
    //     console.log(data.choices[0].message?.content, '<---- groq.com api');
    //     return data.choices[0].message?.content;  // No need to parse JSON again if the API returns text
    //   } else {
    //     console.error(await response.json());
    //     throw new Error('Failed to fetch data from the Groq API');
    //   }
    // }
    
    async function generateResponse(userInput, companyInfo) {
        const messages = [
          {
            role: "system",
            content: `You are an AI assistant for RUGVED SYSTEMS Inc. Answer questions only based on the provided company information: ${JSON.stringify(companyInfo)}. If the question is not related to the provided information, respond with: "I can't answer that question at this moment."`
          },
          { role: "user", content: userInput }
        ];
      
        const requestOptions = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${API_KEY}`
          },
          body: JSON.stringify({
            model: "llama3-8b-8192",  // Replace with the correct Groq model ID
            messages: messages,
            temperature: 0.2,
            top_p: 0.7,
            stream: false,
            stop: null
          })
        };
      
        const response = await fetch(API_URL, requestOptions);
      
        if (response.ok) {
          const data = await response.json();
          console.log(data.choices[0].message?.content, '<---- groq.com api');
          return data.choices[0].message?.content;
        } else {
          console.error(await response.json());
          throw new Error('Failed to fetch data from the Groq API');
        }
      }
    
    // Handle button click
    sendBtn.onclick = async function () {
      if (messageBar.value.length > 0) {
        const userTypedMessage = messageBar.value;
        messageBar.value = "";
    
        // User message element
        const userMessage = `
        <div class="chat message">
          <img src="img/user.jpg">
          <span>${userTypedMessage}</span>
        </div>`;
    
        // Response loading element
        const loadingResponse = `
        <div class="chat response">
          <img src="img/chatbot.png">
          <span class="new">...</span>
        </div>`;
    
        messageBox.insertAdjacentHTML("beforeend", userMessage);
        messageBox.insertAdjacentHTML("beforeend", loadingResponse);
    
        try {
          const responseText = await generateResponse(userTypedMessage, companyInfo);
          const chatBotResponse = document.querySelector(".response .new");
          chatBotResponse.innerHTML = customResponseMiddleware(responseText);
          chatBotResponse.classList.remove("new");
        } catch (error) {
          const chatBotResponse = document.querySelector(".response .new");
          chatBotResponse.innerHTML = `Oops! An error occurred: ${error.message}`;
        }
      }
    };
    </script>
    
</body>
</html>

'''

components.html(html_code, height=400)