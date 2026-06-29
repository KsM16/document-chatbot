// frontend/src/pages/chat/ChatList.tsx
import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { listThreads, createThread } from '../../lib/api';
import type { Thread } from '../../lib/api';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';

export default function ChatList() {
  const { signOut } = useAuth();
  const [threads, setThreads] = useState<Thread[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    listThreads().then(setThreads);
  }, []);

  const handleNewChat = async () => {
    const newThread = await createThread();
    navigate(`/chat/${newThread.id}`);
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">My Chats</h1>
        <div className="flex gap-2">
          <Button onClick={handleNewChat}>+ New Chat</Button>
          <Button variant="outline" onClick={signOut}>Sign Out</Button>
        </div>
      </div>

      <div className="grid gap-4">
        {threads.length === 0 ? (
          <p className="text-center text-gray-500">No chats yet. Start a new one!</p>
        ) : (
          threads.map((thread) => (
            <Link key={thread.id} to={`/chat/${thread.id}`}>
              <Card className="hover:bg-gray-50 transition cursor-pointer">
                <CardHeader>
                  <CardTitle>{thread.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-500">
                    Last updated: {new Date(thread.updated_at).toLocaleString()}
                  </p>
                </CardContent>
              </Card>
            </Link>
          ))
        )}
      </div>
    </div>
  );
}