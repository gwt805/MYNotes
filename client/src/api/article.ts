import http from "../utils/axios";

export const article_add = async (user_id: number, tittle: string, article: string) => {
    return await http.post('article/', {'user_id': user_id, 'title': tittle, "article": article})
}

export const article_get = async (id:number) => {
    return await http.get(`article?id=${id}`)
}

export const article_put = async (id:number, tittle: string, article: string, ) => {
    return await http.put('article/', {'id': id, 'title': tittle, "article": article})
}

export const article_delete = async (id:number) => {
    return await http.post('article/delete/', {"id": id})
}

export const article_search = async (question: string, page_index: number, page_size: number) => {
    return await http.post("article/search/", {"question": question, "page_index": page_index, "page_size": page_size})
}