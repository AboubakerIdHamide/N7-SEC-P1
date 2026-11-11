import axios from 'axios';
export const session=()=>{try{return JSON.parse(sessionStorage.getItem('session'))}catch{return null}};
export const saveSession=(data)=>sessionStorage.setItem('session',JSON.stringify(data));
export const logout=()=>{sessionStorage.removeItem('session');window.location.assign('/login')};
const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://localhost:8080'});
api.interceptors.request.use(config=>{const s=session();if(s?.token)config.headers.Authorization=`Bearer ${s.token}`;return config});
api.interceptors.response.use(r=>r,error=>{if(error.response?.status===401&&!error.config.url.startsWith('/auth/')){sessionStorage.removeItem('session');window.location.assign('/login?expired=1')}return Promise.reject(error)});
export const errorText=e=>e.response?.data?.errors?.join(', ')||e.response?.data?.message||'Cannot reach the server. Check that the backend is running.';
export default api;
