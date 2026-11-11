import api,{saveSession} from './api'; export async function authenticate(mode,data){const r=await api.post('/auth/'+mode,data);saveSession(r.data);return r.data;}
