const API = "https://senthil.onrender.com";
let interval;

async function safeFetch(url, options = {}) {
  try {
    const res = await fetch(url, options);
    const text = await res.text();
    return JSON.parse(text);
  } catch (err) {
    document.getElementById("status").innerText = "❌ " + err.message;
    return null;
  }
}

async function join() {
  let name = document.getElementById("dogName").value.trim();
  if (!name) return alert("Enter dog name");

  let data = await safeFetch(`${API}/join/${name}`, { method: "POST" });

  if (data) {
    document.getElementById("status").innerText = data.message || data.error;
    render();
  }
}

async function startRace() {
  await safeFetch(`${API}/start`, { method: "POST" });

  interval = setInterval(async () => {
    let data = await safeFetch(`${API}/move`, { method: "POST" });

    if (data) {
      render();

      if (data.winner) {
        clearInterval(interval);
        alert("🏆 Winner: " + data.winner);
      }
    }
  }, 500);
}

// 👇 your inline-style render function stays here
