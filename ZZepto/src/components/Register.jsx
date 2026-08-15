import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { registerUser } from "../services/users";

function Register() {
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        password: "",
        confirmPassword: "",
        mobile: "",
    })
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault()
        try {
            const user = await registerUser(formData)
            toast.success(`User registered:  ${user.uid}`)
            navigate("/login")
        }
        catch(err) {
            toast.error(err.message)
        }
    }
    
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value});
    };

    return (
        <div className="container">
            <h2>Register</h2>
            <form onSubmit={handleRegister}>
                <div className="mb-3">
                    <label htmlFor="name" className="form-label">
                        Name
                    </label>
                    <input
                        type="text"
                        className="form-control"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                    />
                </div>
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
                </div>
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
                </div>
                <div className="mb-3">
                    <label htmlFor="confirmPassword" className="form-label">
                        Confirm Password
                    </label>
                    <input
                        type="password"
                        className="form-control"
                        id="confirmPassword"
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="mobile" className="form-label">
                        Mobile
                    </label>
                    <input
                        type="text"
                        className="form-control"
                        id="mobile"
                        name="mobile"
                        value={formData.mobile}
                        onChange={handleChange}
                    />
                </div>
                <button type="submit" className="btn btn-primary">
                    Register
                </button>
            </form>
        </div>
    )



}

export default Register;