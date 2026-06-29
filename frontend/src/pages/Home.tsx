// frontend/src/pages/Home.tsx
import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { http } from '../lib/http';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

interface AuthMeResponse {
  user_id: string;
  email: string;
}

export default function Home() {
  const { user, signOut } = useAuth();
  const [backendUser, setBackendUser] = useState<AuthMeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Call the protected backend endpoint on load
  useEffect(() => {
    async function fetchBackendUser() {
      try {
        // Our http wrapper automatically attaches the Supabase JWT!
        const data = await http<AuthMeResponse>('/auth/me');
        setBackendUser(data);
      } catch (err: unknown) {
            const message =
                err instanceof Error ? err.message : "Failed to fetch from backend";

            setError(message);
            }
    }
    fetchBackendUser();
  }, []);

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Document Copilot</h1>
        <Button variant="outline" onClick={signOut}>Sign Out</Button>
      </div>

      <Card className="mb-4">
        <CardHeader>
          <CardTitle>Frontend Auth State</CardTitle>
        </CardHeader>
        <CardContent>
          <p><strong>Supabase User ID:</strong> {user?.id}</p>
          <p><strong>Email:</strong> {user?.email}</p>
        </CardContent>
      </Card>

      <Card className="mb-4 border-green-500 border-2">
        <CardHeader>
          <CardTitle className="text-green-700">Backend Verification Test</CardTitle>
        </CardHeader>
        <CardContent>
          {error ? (
            <p className="text-red-500">Error: {error}</p>
          ) : backendUser ? (
            <>
              <p className="text-green-700 font-semibold mb-2">Success! JWT reached the backend.</p>
              <p><strong>Backend confirmed User ID:</strong> {backendUser.user_id}</p>
              <p><strong>Backend confirmed Email:</strong> {backendUser.email}</p>
            </>
          ) : (
            <p>Verifying token with backend...</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}