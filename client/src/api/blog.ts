import http from "@/utils/axios";

interface get_blog_single_rep {
    code: number,
    status: string,
    msg: string,
    data ?: {
        "title": string,
        "content": string
    }
}
export const get_blog_single = async (id: number):Promise<get_blog_single_rep> => {
    return await http.get(`/api/blog/getblog/${id}`);
};

interface get_blog_all_rep {
    code: number,
    status: string,
    msg: string,
    data ?: {
        data: {
            "id": number,
            "title": string,
            "content": string
            "created_at": string,
            "updated_at": string
        },
        count: number
    }
}
export const get_blog_all = async (page: number, size: number, search: string):Promise<get_blog_all_rep> => {
    return await http.post("/api/blog/getblog", {page: page, size: size, search: search});
};

interface blog_rep {
    code: number,
    status: string,
    msg: string
}
export const createblog = async (title: string, content: string):Promise<blog_rep> => {
    return await http.post("/api/blog/createblog", {"title": title, "content": content});
};

export const updateblog = async (id: number, title: string, content: string):Promise<blog_rep> => {
    return await http.post("/api/blog/updateblog", {id: id, title: title, content: content});
};

export const deleteblog = async (id: number):Promise<blog_rep> => {
    return await http.post("/api/blog/deleteblog", {id: id});
};