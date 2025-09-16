// Configure API base (change if your backend is elsewhere)
const API_BASE = "http://127.0.0.1:8000";

const statusEl = document.getElementById("status");
const emotionEl = document.getElementById("emotion");
const confEl = document.getElementById("confidence");
const messagesEl = document.getElementById("messages");
const formEl = document.getElementById("chat-form");
const inputEl = document.getElementById("text-input");

async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (res.ok) {
      statusEl.innerHTML = 'Backend: <span class="pill">online</span>';
    } else {
      statusEl.innerHTML = 'Backend: <span class="pill">error</span>';
    }
  } catch (e) {
    statusEl.innerHTML = 'Backend: <span class="pill">offline</span>';
  }
}

function addMessage(text, who = "bot") {
  const div = document.createElement("div");
  div.className = who === "user" ? "user" : "bot";
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = inputEl.value.trim();
  if (!text) return;
  addMessage(text, "user");
  inputEl.value = "";

  try {
    const res = await fetch(`${API_BASE}/predict/text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    emotionEl.textContent = data.emotion;
    confEl.textContent = (data.confidence * 100).toFixed(1) + "%";

    addMessage(data.reply, "bot");

    if (data.crisis === true) {
      addMessage("⚠️ Crisis detected keywords: " + (data.crisis_terms || []).join(", "), "bot");
    }
  } catch (err) {
    addMessage("Sorry, something went wrong connecting to the server.", "bot");
  }
});

checkHealth();
