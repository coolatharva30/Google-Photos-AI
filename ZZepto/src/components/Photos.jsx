import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import {
    uploadPhoto,
    getPhotos,
    getPhotoUrl,
    deletePhoto
} from "../services/photos";


function Photos() {

    const navigate = useNavigate();

    const fileInputRef = useRef(null);

    const [photos, setPhotos] = useState([]);

    const user = JSON.parse(
        sessionStorage.getItem("user")
    );


    useEffect(() => {

        if (!user) {
            navigate("/login");
            return;
        }

        loadPhotos();

    }, []);


    const loadPhotos = async () => {

        try {

            const data = await getPhotos(user.uid);
            console.log("Photo recieved:", data);
            setPhotos(data);

        } catch (error) {

            toast.error(
                error.response?.data?.detail ||
                "Unable to load photos"
            );

        }
    };


    const handleUpload = async (file) => {

        if (!file) {
            return;
        }

        try {

            await uploadPhoto(
                user.uid,
                file
            );
            
            toast.success(
                "Photo uploaded successfully"
            );

            await loadPhotos();

        } catch (error) {

            toast.error(
                error.response?.data?.detail ||
                "Upload failed"
            );

        }
    };


    const handleDelete = async (photoId) => {
        
       
        const confirmDelete = window.confirm(
            "Are you sure you want to delete this photo?"
        );

        if (!confirmDelete) {
            return;
        }

        try {
            console.log("Calling deletePhoto...");
            const response = await deletePhoto(
                user.uid,
                photoId
            );
            console.log("Delete response:", response);
            toast.success(
                "Photo deleted successfully"
            );

            setPhotos(prevPhotos =>
                prevPhotos.filter(
                    photo => photo.id !== photoId
                )
            );

        } catch (error) {

            toast.error(
                error.response?.data?.detail ||
                "Failed to delete photo"
            );

        }
};

    const handleFileSelect = (event) => {

        const file = event.target.files[0];

        handleUpload(file);

        event.target.value = "";

    };


    const handleLogout = () => {

        sessionStorage.removeItem("token");
        sessionStorage.removeItem("user");

        navigate("/login");

    };


    if (!user) {
        return null;
    }


    return (

        <div className="photos-page">

            {/* HEADER */}

            <nav className="navbar navbar-light bg-white shadow-sm px-4">

                <div>

                    <h4 className="mb-0">
                        My Photos
                    </h4>

                </div>


                <div className="d-flex align-items-center gap-3">

                    <span>
                        Hi, <strong>{user.name}</strong>
                    </span>

                    <button
                        className="btn btn-outline-danger"
                        onClick={handleLogout}
                    >
                        Logout
                    </button>

                </div>

            </nav>


            {/* BODY */}

            <div className="container mt-4">

                {/* UPLOAD AREA */}

                <div className="card p-4 mb-4">

                    <div className="d-flex gap-2">

                        <button
                            className="btn btn-primary"
                            onClick={() =>
                                fileInputRef.current.click()
                            }
                        >
                            📁 Upload Photo
                        </button>

                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="image/*"
                            style={{
                                display: "none"
                            }}
                            onChange={
                                handleFileSelect
                            }
                        />

                    </div>

                </div>


                {/* PHOTO GRID */}

                <h4 className="mb-3">
                    Your Photos
                </h4>


                {photos.length === 0 ? (

                    <div className="text-center mt-5">

                        <h5>
                            No photos yet
                        </h5>

                        <p>
                            Upload your first photo.
                        </p>

                    </div>

                ) : (

                    <div className="row g-3">

                        {photos.map(photo => (

                            <div
                                key={photo.id}
                                className="col-6 col-md-4 col-lg-3"
                            >

                                <div className="card">

                                    <img
                                        src={getPhotoUrl(
                                            user.uid,
                                            photo.id
                                        )}
                                        alt={photo.filename}
                                        style={{
                                            width: "100%",
                                            height: "220px",
                                            objectFit: "cover"
                                        }}
                                    />
                                        <div className="p-2">

                                            <button
                                                className="btn btn-danger btn-sm w-100"
                                                onClick={() => handleDelete(photo.id)}
                                            >
                                                🗑️ Delete
                                            </button>

                                        </div>

                                </div>

                            </div>

                        ))}

                    </div>

                )}

            </div>

        </div>
    );
}


export default Photos;