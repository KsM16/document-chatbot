// frontend/src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js';
import { env } from './env';

// This is the single instance of the Supabase client for the entire frontend
export const supabase = createClient(env.supabaseUrl, env.supabaseAnonKey);