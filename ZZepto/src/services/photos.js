import axios from "axios";
import { BASE_URL } from "./config"

export async function uploadPhoto(userId, file,latitude,longitude){
    console.log("photos.js userId:", userId);
    console.log("photos.js latitude:", latitude);
    console.log("photos.js longitude:", longitude);
    const formData = new FormData();

    formData.append("file", file);

    const response = await axios.post(
        `${BASE_URL}photos/upload?user_id=${userId}&latitude=${latitude}&longitude=${longitude}`,
        formData
    );

    return response.data;
}

export async function getPhotos(userId) {

    const response = await axios.get(
        `${BASE_URL}photos/?user_id=${userId}`
    );

    return response.data.data;
}

export function getPhotoUrl(
    userId,
    photoId
){
    return `${BASE_URL}photos/${photoId}?user_id=${userId}`
}

export async function deletePhoto(
    userId,
    photoId
) {
    const response = await axios.delete(`${BASE_URL}photos/${photoId}?user_id=${userId}`);
    return response.data;
}