import axios from "axios";
import { BASE_URL } from "./config"

export async function uploadPhoto(userId, file){

    const formData = new formData();

    formData.append("file", file);

    const response = await axios.post(
        `${BASE_URL}photos/upload?user_id=${userId}`,
        formData
    );

    return response.data;
}

export async function getPhotos(userId) {

    const response = await axios.get(
        `${BASEURL}photos/?user_id=${userId}`
    );

    return response.data.data;
}

export function getPhotoUrl(
    userId,
    photoId
){
    return `${BASE_URL}photos/${photoId}?user_id=${userId}`
}