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
    const [selectedPhoto, setSelectedPhoto] = useState(null);

    const user = JSON.parse(
        sessionStorage.getItem("user")
    );


    const getCurrentLocation = () => {

        return new Promise((resolve, reject) => {
            if(!navigator.geolocation){
                reject(
                    new Error("Geolocation is not supported by this browser")
                );
                return;
            }

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    console.log(
                    "Raw latitude:",
                    position.coords.latitude
                );

                console.log(
                    "Raw longitude:",
                    position.coords.longitude
                );
                    resolve({
                        latitude:position.coords.latitude,
                        longitude:position.coords.longitude,
                    });
                },

                (error) => {
                    reject(error)
                },
                {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
            );
        });
    };





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
            const location = await getCurrentLocation();
            console.log("Latitude:", location.latitude);
            console.log("Longitude:", location.longitude);
            await uploadPhoto(
                user.uid,
                file,
                location.latitude,
                location.longitude
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



            {selectedPhoto && (

                <div
                    onClick={() => setSelectedPhoto(null)}
                    style={{
                        position: "fixed",
                        top: 0,
                        left: 0,
                        width: "100%",
                        height: "100%",
                        backgroundColor: "rgba(0, 0, 0, 0.9)",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        zIndex: 1050,
                        padding: "20px"
                    }}
                >

                    <button
                        onClick={() => setSelectedPhoto(null)}
                        style={{
                            position: "absolute",
                            top: "20px",
                            right: "30px",
                            background: "transparent",
                            border: "none",
                            color: "white",
                            fontSize: "35px",
                            cursor: "pointer"
                        }}
                    >
                        ×
                    </button>

                    <img
                        src={getPhotoUrl(
                            user.uid,
                            selectedPhoto.id
                        )}
                        alt={selectedPhoto.filename}
                        onClick={(event) => event.stopPropagation()}
                        style={{
                            maxWidth: "95%",
                            maxHeight: "90%",
                            objectFit: "contain"
                        }}
                    />

                </div>

            )}
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
                                        onClick={() => setSelectedPhoto(photo)}
                                        style={{
                                            width: "100%",
                                            height: "220px",
                                            objectFit: "cover",
                                            cursor: "pointer"
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