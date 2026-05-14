import { useState } from "react";

function Register() {
  const [userName, setUserName] = useState("");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  async function registerUser(e: React.ChangeEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (userName.length < 3) {
      setError("El usuario debe tener mínimo 3 caracteres");
      return;
    }

    if (fullName.length < 3) {
      setError("El nombre completo debe tener mínimo 3 caracteres");
      return;
    }

    if (!emailRegex.test(email)) {
      setError("Correo invalido");
      return;
    }

    if (password.length < 6) {
      setError("La contraseña debe tener mínimo 6 caracteres");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userName,
          full_name: fullName,
          email,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        if (Array.isArray(data.detail)) {
          throw new Error(data.detail[0].msg);
        }
        throw new Error(data.detail);
      }

      setSuccess("Usuario registrado correctamente");

      setTimeout(() => {
        setSuccess("");
      }, 3000);

      setUserName("");
      setFullName("");
      setEmail("");
      setPassword("");
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      }
    }
  }

  return (
    <form className="form" onSubmit={registerUser}>
      <h1>Registrar usuario</h1>

      <label>Nombre de usuario</label>
      <input
        required
        type="text"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />

      <label>Nombre completo</label>
      <input
        required
        type="text"
        value={fullName}
        onChange={(e) => setFullName(e.target.value)}
      />

      <label>Correo electronico</label>
      <input
        required
        type="text"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <label>Contraseña</label>
      <input
        required
        type="text"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button>Registrar</button>

      {error && <p className="errorMessage">{error}</p>}
      {success && <p className="successMessage">{success}</p>}
    </form>
  );
}

export default Register;
