const configuredApi = import.meta.env.VITE_API_URL

export const API = configuredApi || (import.meta.env.DEV ? 'http://localhost:5000/api' : '/api')
