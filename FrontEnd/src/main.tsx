import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

import { createBrowserRouter, RouterProvider } from "react-router-dom"
import Login from './routes/Login.tsx'
import Register from './routes/Register.tsx'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Login/>
  },
  {
    path: "/register",
    element: <Register/>
  }
])


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router = {router}/>
  </StrictMode>,
)
