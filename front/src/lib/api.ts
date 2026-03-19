export interface ApiError {
  error: string;
}

const API_BASE = 'http://localhost:5000';

export const fetchApi = async <T>(url: string, options: RequestInit = {}): Promise<T> => {
  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(errorData.error || 'Request failed');
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
};

export const actorApi = {
  register: (username: string, password: string) => 
    fetchApi('/api/auth/register', { method: 'POST', body: JSON.stringify({ username, password }) }),
  login: (username: string, password: string) => 
    fetchApi('/api/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) }),
  list: () => 
    fetchApi<any[]>('/api/actors'),
  follow: (targetId: string) => 
    fetchApi(`/api/follow/${targetId}`, { method: 'POST' }),
  unfollow: (targetId: string) => 
    fetchApi(`/api/follow/${targetId}`, { method: 'DELETE' }),
  deleteActor: (actorId: string) => 
    fetchApi(`/api/actors/${actorId}`, { method: 'DELETE' }),
};

export const noteApi = {
  create: (content: string, attachments?: any[]) => 
    fetchApi('/api/notes', { method: 'POST', body: JSON.stringify({ content, attachments }) }),
  list: () => 
    fetchApi<any[]>('/api/notes'),
  delete: (noteId: string) => 
    fetchApi(`/api/notes/${noteId}`, { method: 'DELETE' }),
};
