import { useState } from "react";

function Login() {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState<string>("");

  async function loginUser(e: React.ChangeEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (username.length < 3) {
      setError("El usuario debe tener mínimo 3 caracteres");
      return;
    }

    if (password.length < 6) {
      setError("La contraseña debe tener mínimo 6 caracteres");
      return;
    }

    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData.toString(),
        credentials: "include",
      });

      const data = await response.json();

      if (!response.ok) {
        if (Array.isArray(data.detail)) {
          throw new Error(data.detail[0].msg);
        }
        throw new Error(data.detail);
      }

      setSuccess("Usuario logueado correctamente");

      setTimeout(() => {
        setSuccess("");
      }, 3000);

      setUsername("");
      setPassword("");
    } catch (error) {
      console.log("Error al iniciar sesión:", error);
      if (error instanceof Error) {
        setError(error.message);
      }
    }
  }

  return (
    <form className="form" onSubmit={loginUser}>
      <h1>Iniciar sesión</h1>

      <label>Nombre de usuario</label>
      <input
        required
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <label>Contraseña</label>
      <input
        required
        type="text"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button>Entrar</button>

      {error && <p className="errorMessage">{error}</p>}
      {success && <p className="successMessage">{success}</p>}
    </form>
  );
}
export default Login;
