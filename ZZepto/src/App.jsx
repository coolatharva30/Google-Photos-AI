import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import AuthProvider from './providers/authenticator'
import ThemeProvider from './providers/themeprovider'
import {Route, Routes } from 'react-router-dom'
import Register from './components/Register'
import Login from './components/Login'
import Logout from './components/Logout'
import Photos from './components/Photos'

function App() {
   const [count, setCount] = useState(0)

   return (
    <>
      <AuthProvider>
       <ThemeProvider> 


         <div className="d-flex justify-content-center">
          <h1>Photos</h1>
        </div>
          <Routes>

            <Route index element={<Login />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register/>} />
            <Route path="/logout" element={<Logout/>} />
            <Route path="/photos" element={<Photos />} />

          </Routes>~
    
         </ThemeProvider>
      </AuthProvider> 
      </>
    
  );
}

export default App
