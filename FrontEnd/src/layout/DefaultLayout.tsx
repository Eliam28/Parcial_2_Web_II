import { Link } from "react-router-dom"

interface DefaultLayoutProps {
    children: React.ReactNode;
}

function DefaultLayout({children}: DefaultLayoutProps){
    return <>
        <header>
            <nav>
                <ul>
                    <li>
                        <Link to = "/">Login</Link>
                    </li>
                     <li>
                        <Link to = "/register">Register</Link>
                    </li>
                </ul>
            </nav>

        </header>

        <main>
            {children}
        </main>

    </>
}

export default DefaultLayout