// frontend/src/lib/api.ts
import { http } from './http';

export interface HealthCheckResponse {
  status: string;
}

export async function checkHealth(): Promise<HealthCheckResponse> {
  return http<HealthCheckResponse>('/health');
}

export interface Thread {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export async function listThreads(): Promise<Thread[]> {
  return http<Thread[]>('/threads');
}

export async function createThread(): Promise<Thread> {
  return http<Thread>('/threads', { method: 'POST' });
}

export async function getMessages(threadId: string): Promise<Message[]> {
  return http<Message[]>(`/threads/${threadId}/messages`);
}