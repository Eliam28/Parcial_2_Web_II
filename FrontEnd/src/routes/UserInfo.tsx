import { useState } from "react";

function UserInfo() {
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState<string>("");

  async function fetchUserInfo() {
    try {
      const response = await fetch("http://127.0.0.1:8000/users/me", {
        method: "GET",
        credentials: "include",
      });

      const data = await response.json();

      if (!response.ok) {
        if (Array.isArray(data.detail)) {
          throw new Error(data.detail[0].msg);
        }
        throw new Error(data.detail);
      }

      setSuccess(
        `Usuario: ${data.userName}, Nombre completo: ${data.full_name}, Email: ${data.email}`,
      );
    } catch (error) {
      console.log(error);
      setError("Error al obtener la información del usuario");
    }
  }

  return (
    <div className="form">
      <h1>Información del usuario</h1>
      <button onClick={fetchUserInfo}>Mostrar información</button>
      {error && <p className="errorMessage">{error}</p>}
      {success && <p className="successMessage">{success}</p>}
    </div>
  );
}

export default UserInfo;
