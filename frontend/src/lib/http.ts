// frontend/src/lib/http.ts
import { supabase } from './supabase';
import { env } from './env';

export class HttpError extends Error {
  constructor(public status: number, public message: string) {
    super(message);
  }
}

async function getAuthHeaders(): Promise<Record<string, string>> {
  // Get the current session from Supabase
  const { data: { session } } = await supabase.auth.getSession();
  if (session?.access_token) {
    return { Authorization: `Bearer ${session.access_token}` };
  }
  return {};
}

export async function http<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const authHeaders = await getAuthHeaders();
  
  const response = await fetch(`${env.apiBaseUrl}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders,
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new HttpError(response.status, errorText);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}