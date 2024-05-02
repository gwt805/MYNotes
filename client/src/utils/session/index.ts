export const setSession = (access_token: string, refresh_token:string, expires_in: number, created_at: number, user_id: number, name: string, avatar_url: string, email: string) => {
    localStorage.setItem("access_token", access_token)
    localStorage.setItem("refresh_token", refresh_token)
    localStorage.setItem("expires_in", String(expires_in))
    localStorage.setItem("created_at", String(created_at))
    localStorage.setItem("user_id", String(user_id))
    localStorage.setItem("name", name)
    localStorage.setItem("avatar_url", avatar_url)
    localStorage.setItem("email", email)
}

export const getSession = () => {
    return {
        "access_token": localStorage.getItem("access_token"),
        "refresh_token": localStorage.getItem("refresh_token"),
        "expires_in": Number(localStorage.getItem("expires_in")),
        "created_at": Number(localStorage.getItem("created_at")),
        "user_id": Number(localStorage.getItem("user_id")),
        "name": localStorage.getItem("name"),
        "avatar_url": localStorage.getItem("avatar_url"),
        "email": localStorage.getItem("email")
    }
}

export const clearSession = () => {
    window.localStorage.clear()
}

export const is_expire = (created_at: number = getSession().created_at, expires_in: number = getSession().expires_in) => {
    const expirationDate = new Date(0);
    expirationDate.setSeconds(expires_in + created_at);

    const now = new Date().getTime();

    if (now > expirationDate.getTime()) { return true; }
    else { return false; }
}

export const nullSession = () => {
    const {access_token, refresh_token, expires_in, created_at, user_id, name, avatar_url, email} = getSession()
    if (access_token == null || refresh_token == null || expires_in == 0 || created_at == 0 || user_id == 0 || name == null || avatar_url == null || email == null) {
        return true
    }
    else {
        return false
    }
}

// 指定距离token失效时间 进行刷新token
export const miss_token = (created_at: number = getSession().created_at, expires_in: number = getSession().expires_in) => {
    const timestamp = expires_in + created_at; // 给定的时间戳，假设是秒为单位
    const timestampMs = timestamp * 1000; // 将时间戳转换为毫秒
    const nowMs = Date.now(); // 获取当前时间的时间戳（毫秒）
    const timeDifferenceMs = timestampMs - nowMs; // 计算当前时间与给定时间戳的差值（毫秒）

    // 判断是否只剩下1分钟（60000毫秒）
    if (timeDifferenceMs === 60000) {
        return true
    }
    else {
        return false
    }
}