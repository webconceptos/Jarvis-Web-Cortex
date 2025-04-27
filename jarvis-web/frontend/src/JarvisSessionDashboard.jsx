import { useState, useEffect, useRef } from "react";

function JarvisSessionDashboard({ onLogout }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const recognitionRef = useRef(null);

  useEffect(() => {
    if (!('webkitSpeechRecognition' in window)) {
      alert("Tu navegador no soporta reconocimiento de voz");
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "es-ES";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInputText(transcript);
    };

    recognitionRef.current = recognition;
  }, []);

  const startListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start();
    }
  };

  const handleSend = async () => {
    if (!inputText.trim()) return;
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username") || "user";

    const newMessages = [...messages, { role: "user", content: inputText }];
    setMessages(newMessages);
    setInputText("");

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ prompt: inputText, session_id: username }),
      });

      const data = await response.json();
      if (data.response) {
        const updatedMessages = [...newMessages, { role: "assistant", content: data.response }];
        setMessages(updatedMessages);

        // Reproducir respuesta
        const speakResponse = await fetch("/api/speak", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ prompt: data.response }),
        });

        if (speakResponse.ok) {
          const blob = await speakResponse.blob();
          const url = URL.createObjectURL(blob);
          const audio = new Audio(url);
          audio.play();
        }
      }
    } catch (error) {
      console.error("Error enviando mensaje:", error);
    }
  };

  return (
    <div className="dashboard-container">
      <h2>Jarvis Web - Sesión Activa</h2>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={msg.role}>
            <b>{msg.role === "user" ? "Tú" : "Jarvis"}:</b> {msg.content}
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={inputText}
          placeholder="Escribe o usa el micrófono..."
          onChange={(e) => setInputText(e.target.value)}
        />
        <button onClick={handleSend}>Enviar</button>
        <button onClick={startListening}>🎤</button>
        <button onClick={onLogout}>Salir</button>
      </div>
    </div>
  );
}

export default JarvisSessionDashboard;
