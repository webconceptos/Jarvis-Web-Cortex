import { useState } from "react";

function JarvisLoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [registerMode, setRegisterMode] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const url = registerMode ? "/api/register" : "/api/token";
      const options = registerMode
        ? {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
          }
        : {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ username, password }),
          };

      const response = await fetch(url, options);
      const data = await response.json();

      if (registerMode) {
        if (response.ok) {
          alert("Usuario registrado correctamente. Ahora puedes iniciar sesión.");
          setRegisterMode(false);
        } else {
          setError(data.detail || "Error de registro");
        }
      } else {
        if (response.ok && data.access_token) {
          localStorage.setItem("token", data.access_token);
          localStorage.setItem("username", username);
          onLoginSuccess();
        } else {
          setError(data.detail || "Credenciales inválidas");
        }
      }
    } catch (error) {
      setError("Error de conexión");
    }
  };

  return (
    <div className="login-container">
      <h2>{registerMode ? "Registrar Usuario" : "Iniciar Sesión"}</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">
          {registerMode ? "Registrar" : "Entrar"}
        </button>
      </form>
      <button onClick={() => setRegisterMode(!registerMode)}>
        {registerMode ? "¿Ya tienes cuenta? Iniciar Sesión" : "¿No tienes cuenta? Registrarse"}
      </button>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default JarvisLoginPage;
