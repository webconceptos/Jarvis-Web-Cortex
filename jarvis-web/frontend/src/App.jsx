import { useState, useEffect } from "react";
import JarvisLoginPage from "./JarvisLoginPage";
import JarvisSessionDashboard from "./JarvisSessionDashboard";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken(null);
  };

  const handleLoginSuccess = () => {
    setToken(localStorage.getItem("token"));
  };

  useEffect(() => {
    const checkToken = () => {
      const storedToken = localStorage.getItem("token");
      setToken(storedToken);
    };
    checkToken();
  }, []);

  if (!token) {
    return <JarvisLoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <JarvisSessionDashboard onLogout={handleLogout} />
  );
}

export default App;
