import http from "@/utils/axios";

interface usually_rep {
    code: number,
    status: string,
    msg: string
}
export const register = async (username: string, password: string):Promise<usually_rep> => {
    return await http.post("/api/auth/register", {username: username, password: password});
};

interface login_rep {
    code: number,
    status: string,
    msg: string,
    data?: {
        'username': string,
        'avatar': string,
        'isadmin': boolean,
        'created_at': string,
        'updated_at': string,
        'token': string
    }
}
export const login = async (username: string, password: string):Promise<login_rep> => {
    return await http.post("/api/auth/login", {username: username, password: password});
};

export const updatepwd = async (id: number, password: string) => {
    return await http.post("/api/auth/changepwd", {id: id, password: password});
};

export const updateuserimg = async (id: number, avatar: string):Promise<usually_rep> => {
    return await http.post("/api/auth/update/avatar", {id: id, avatar: avatar});
};

export const get_user_info = async (username: string) => {
    return await http.post("/api/auth/get_user_info/", {username: username});
};