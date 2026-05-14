import { Link } from "react-router-dom";

interface DefaultLayoutProps {
  children: React.ReactNode;
}

function Navbar() {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/login">Login</Link>
        </li>
        <li>
          <Link to="/register">Register</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
