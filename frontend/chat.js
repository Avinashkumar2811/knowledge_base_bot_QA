console.log("chat.js loaded");

const chatBtn = document.getElementById("chat-btn");
const chatbox = document.getElementById("chatbox");

chatBtn.onclick = () => {
  chatbox.style.display = "block";
};

// async function sendMessage() {
//   const input = document.getElementById("input");
//   const msg = input.value;
//   if (!msg) return;

//   const messages = document.getElementById("messages");
//   messages.innerHTML += `<p><b>You:</b> ${msg}</p>`;
//   input.value = "";

//   const res = await fetch("http://127.0.0.1:9067/ask", {
//     method: "POST",
//     headers: {"Content-Type": "application/json"},
//     body: JSON.stringify({ question: msg })
//   });

//   const data = await res.json();
//   messages.innerHTML += `<p><b>Bot:</b> ${data.answer}</p>`;
// }

async function sendMessage() {
  console.log("sendMessage triggered");

  const input = document.getElementById("input");
  const msg = input.value.trim();
  if (!msg) return;

  const messages = document.getElementById("messages");
  messages.innerHTML += `<p><b>You:</b> ${msg}</p>`;
  input.value = "";

  try {
    const res = await fetch("http://127.0.0.1:9067/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: msg })
    });

    console.log("Response status:", res.status);

    const data = await res.json();
    console.log("Response data:", data);

    messages.innerHTML += `<p><b>Bot:</b> ${data.answer}</p>`;
  } catch (err) {
    console.error("Fetch error:", err);
    messages.innerHTML += `<p><b>Bot:</b> Error connecting to server</p>`;
  }
}
