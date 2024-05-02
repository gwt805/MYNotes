import { ElMessage } from 'element-plus';

export const public_elmsg_info = (msg: string, duration:number = 1000) => {
    ElMessage({ type: 'info', message: msg, duration: duration })
};

export const public_elmsg_success = (msg: string, duration:number = 1000) => {
    ElMessage({ type: 'success', message: msg, duration: duration })
};

export const public_elmsg_warning = (msg: string, duration:number = 1000) => {
    ElMessage({ type: 'warning', message: msg, duration: duration })
};

export const public_elmsg_error = (msg: string, duration:number = 1000) => {
    ElMessage({ type: 'error', message: msg, duration: duration })
};