import http from "../utils/axios";

export const get_client_id_secret = async() => {
    return await http.get("login/")
}

export const login = async (username: string, password: string) => {
    return await http.post('login/', {'username': username, "password": password})
}