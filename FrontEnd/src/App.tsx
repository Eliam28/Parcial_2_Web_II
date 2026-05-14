import { Navigate, Route, Routes } from "react-router-dom";
import "./App.css";
import Login from "./routes/Login";
import Register from "./routes/Register";
import Navbar from "./layout/Navbar";
import UserInfo from "./routes/UserInfo";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/user-info" element={<UserInfo />} />
      </Routes>
    </>
  );
}

export default App;
