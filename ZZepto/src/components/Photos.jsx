import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import {
    uploadPhoto,
    getPhotos,
    getPhotoUrl,
    deletePhoto
} from "../services/photos";

import "./Photos.css";


function Photos() {

    const navigate = useNavigate();

    const fileInputRef = useRef(null);

    const [photos, setPhotos] = useState([]);
    const [selectedPhoto, setSelectedPhoto] = useState(null);

    const user = JSON.parse(
        sessionStorage.getItem("user")
    );


    // =========================================================
    // GET CURRENT LOCATION
    // =========================================================

    const getCurrentLocation = () => {

        return new Promise((resolve, reject) => {

            if (!navigator.geolocation) {

                reject(
                    new Error(
                        "Geolocation is not supported by this browser"
                    )
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
                        latitude:
                            position.coords.latitude,

                        longitude:
                            position.coords.longitude
                    });
                },

                (error) => {
                    reject(error);
                },

                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        });
    };


    // =========================================================
    // LOAD PHOTOS
    // =========================================================

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

            console.log(
                "Photos received:",
                data
            );

            setPhotos(data);

        } catch (error) {

            console.error(
                "Load photos error:",
                error
            );

            toast.error(
                error.response?.data?.detail ||
                "Unable to load photos"
            );
        }
    };


    // =========================================================
    // UPLOAD PHOTO
    // =========================================================

    const handleUpload = async (file) => {

        if (!file) {
            return;
        }

        try {

            const location =
                await getCurrentLocation();

            console.log(
                "Latitude:",
                location.latitude
            );

            console.log(
                "Longitude:",
                location.longitude
            );

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

            console.error(
                "Upload error:",
                error
            );

            toast.error(
                error.response?.data?.detail ||
                "Upload failed"
            );
        }
    };


    // =========================================================
    // FILE SELECT
    // =========================================================

    const handleFileSelect = (event) => {

        const file =
            event.target.files[0];

        handleUpload(file);

        event.target.value = "";
    };


    // =========================================================
    // DELETE PHOTO
    // =========================================================

    const handleDelete = async (photoId) => {

        const confirmDelete =
            window.confirm(
                "Are you sure you want to delete this photo?"
            );

        if (!confirmDelete) {
            return;
        }

        try {

            console.log(
                "Deleting photo:",
                photoId
            );

            const response =
                await deletePhoto(
                    user.uid,
                    photoId
                );

            console.log(
                "Delete response:",
                response
            );

            toast.success(
                "Photo deleted successfully"
            );

            setPhotos((prevPhotos) =>
                prevPhotos.filter(
                    (photo) =>
                        photo.id !== photoId
                )
            );

            if (
                selectedPhoto &&
                selectedPhoto.id === photoId
            ) {
                setSelectedPhoto(null);
            }

        } catch (error) {

            console.error(
                "Delete error:",
                error
            );

            toast.error(
                error.response?.data?.detail ||
                "Failed to delete photo"
            );
        }
    };


    // =========================================================
    // LOGOUT
    // =========================================================

    const handleLogout = () => {

        sessionStorage.removeItem("token");

        sessionStorage.removeItem("user");

        navigate("/login");
    };


    // =========================================================
    // NOT LOGGED IN
    // =========================================================

    if (!user) {
        return null;
    }


    // =========================================================
    // UI
    // =========================================================

    return (

        <div className="photos-page">


            {/* =====================================================
                FULL SCREEN PHOTO VIEW
            ====================================================== */}

            {selectedPhoto && (

                <div
                    className="photo-viewer"
                    onClick={() =>
                        setSelectedPhoto(null)
                    }
                >

                    {/* CLOSE BUTTON */}

                    <button
                        className="photo-viewer-close"
                        onClick={() =>
                            setSelectedPhoto(null)
                        }
                    >
                        ×
                    </button>


                    {/* LARGE PHOTO */}

                    <img
                        className="photo-viewer-image"

                        src={getPhotoUrl(
                            user.uid,
                            selectedPhoto.id
                        )}

                        alt={
                            selectedPhoto.filename
                        }

                        onClick={(event) =>
                            event.stopPropagation()
                        }
                    />

                </div>
            )}


            {/* =====================================================
                HEADER
            ====================================================== */}

            <nav className="photos-navbar">


                {/* LEFT SIDE */}

                <div className="photos-logo">

                    <span className="photos-logo-icon">
                        📷
                    </span>

                    <span className="photos-logo-text">
                        Photos
                    </span>

                </div>


                {/* RIGHT SIDE */}

                <div className="photos-user-section">


                    {/* USER NAME */}

                    <span className="photos-user-name">
                        {user.name}
                    </span>


                    {/* PROFILE CIRCLE */}

                    <div
                        className="photos-profile-circle"
                        title={user.name}
                    >
                        {user.name
                            ? user.name.charAt(0).toUpperCase()
                            : "U"}
                    </div>


                    {/* LOGOUT */}

                    <button
                        className="photos-logout-button"
                        onClick={handleLogout}
                    >
                        Logout
                    </button>

                </div>

            </nav>


            {/* =====================================================
                MAIN CONTENT
            ====================================================== */}

            <main className="photos-main">


                {/* =================================================
                    UPLOAD SECTION
                ================================================== */}

                <section className="upload-card">

                    <div className="upload-card-content">


                        {/* LEFT */}

                        <div>

                            <h5 className="upload-title">
                                Add photos
                            </h5>

                            <small className="upload-description">
                                Upload photos to your gallery
                            </small>

                        </div>


                        {/* RIGHT */}

                        <div>

                            <button
                                className="upload-button"
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
                                className="hidden-file-input"
                                onChange={
                                    handleFileSelect
                                }
                            />

                        </div>

                    </div>

                </section>


                {/* =================================================
                    PHOTO HEADER
                ================================================== */}

                <div className="photos-heading">

                    <div>

                        <h4 className="photos-title">
                            Your Photos
                        </h4>

                        <small className="photos-count">
                            {photos.length}{" "}

                            {photos.length === 1
                                ? "photo"
                                : "photos"}
                        </small>

                    </div>

                </div>


                {/* =================================================
                    EMPTY GALLERY
                ================================================== */}

                {photos.length === 0 ? (

                    <div className="empty-gallery">

                        <div className="empty-gallery-icon">
                            🖼️
                        </div>

                        <h5>
                            No photos yet
                        </h5>

                        <p className="empty-gallery-text">
                            Upload your first photo
                            to get started.
                        </p>

                        <button
                            className="upload-button"
                            onClick={() =>
                                fileInputRef.current.click()
                            }
                        >
                            📁 Upload Photo
                        </button>

                    </div>

                ) : (


                    /* =================================================
                       GOOGLE PHOTOS STYLE GRID
                    ================================================== */

                    <div className="photos-grid">

                        {photos.map((photo) => (

                            <div
                                key={photo.id}
                                className="photo-thumbnail"
                            >


                                {/* PHOTO */}

                                <img
                                    src={getPhotoUrl(
                                        user.uid,
                                        photo.id
                                    )}

                                    alt={
                                        photo.filename
                                    }

                                    onClick={() =>
                                        setSelectedPhoto(
                                            photo
                                        )
                                    }

                                    className="photo-thumbnail-image"
                                />


                                {/* DELETE BUTTON */}

                                <button
                                    className="photo-delete-button"

                                    onClick={(event) => {

                                        event.stopPropagation();

                                        handleDelete(
                                            photo.id
                                        );

                                    }}

                                    title="Delete photo"
                                >
                                    🗑️
                                </button>

                            </div>

                        ))}

                    </div>

                )}

            </main>

        </div>
    );
}


export default Photos;