import { BASE_URL } from "./config";
import axios from "axios";

export async function findUserByCredentials(cred) {
    const url = BASE_URL + "users/authenticate";

    const response = await axios.post(url, cred);

    if (response.status === 200) {
        const resp = response.data;

        if (resp.status === "success") {
            return resp.data;
        }

        throw new Error("Error: " + resp.error);
    }

    throw new Error(`Error Status: ${response.status}`);
}

export async function registerUser(formData) {
    const response = await axios.post(
        BASE_URL + "users/register",
        formData
    );

    return response.data;
}