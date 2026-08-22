import { Link,useNavigate } from "react-router-dom";
import { useAuth } from "../providers/authenticator";
import { findUserByCredentials } from "../services/users";
import { toast} from 'react-toastify'
import { useState } from "react";

function Login() {
   const [formData, setFormData] = useState({
       email: "",
       password: "",
   })
   const navigate = useNavigate();
   const {setUser} = useAuth();
   

   const handleLogin = async (e) => {
    e.preventDefault();
    try {
        const cred = {email: formData.email, passwd: formData.password}
        const user = await findUserByCredentials(cred)

        sessionStorage.setItem("token", user.token)

        sessionStorage.setItem("user", JSON.stringify(user))
        setUser(user)
        toast.success("Welcome, " + user.name)
        navigate("/photos") 
    }
    catch(err) {
       toast.error(err.message)
    }
   };


   const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value});
   }


   return (
    <div className="container">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
            <div className="mb-3">
                <label htmlFor="email" className="form-label">
                    Email
                </label>
                 <input
                        type="email"
                        className="form-control"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                    />
                    <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                        Password
                    </label>
                    <input
                        type="password"
                        className="form-control"
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                    />
                    <button type="submit" className="btn btn-primary">
                    Sign In
                    </button>
                    <Link to="/register" className="btn btn-secondary">Sign Up</Link>
                    </div>
            </div>
        </form>

    </div>
   )




}

 export default Login;