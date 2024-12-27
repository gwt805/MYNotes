import http from "@/utils/axios";

interface return_rep {
    code: number,
    status: string,
    msg: string
}

export const uploadfile = async (data: FormData):Promise<return_rep> => {
    return await http.post("/api/file/upload", data, {headers: {'Content-Type': 'multipart/form-data'}});
};

export const removefile = async (username: string, password: string):Promise<return_rep> => {
    return await http.post("/api/file/delete", {username: username, password: password});
};