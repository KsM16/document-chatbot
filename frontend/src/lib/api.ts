// frontend/src/lib/api.ts
import { http } from './http';

export interface HealthCheckResponse {
  status: string;
}

export async function checkHealth(): Promise<HealthCheckResponse> {
  return http<HealthCheckResponse>('/health');
}

// We will add more API calls here in Phase 3 (Chat shell)