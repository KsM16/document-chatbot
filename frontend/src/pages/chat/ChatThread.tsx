// frontend/src/pages/chat/ChatThread.tsx
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { supabase } from '../../lib/supabase';
import { env } from '../../lib/env';
import { getMessages, type Message } from '../../lib/api'; // <-- Fixed import
import { Button } from '../../components/ui/button';
import { Card, CardContent } from '../../components/ui/card';

export default function ChatThread() {
  const { threadId } = useParams<{ threadId: string }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Load messages
  useEffect(() => {
    if (threadId) {
      getMessages(threadId).then(setMessages);
    }
  }, [threadId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !threadId || isLoading) return;

    setIsLoading(true);
    const userMessage = input;
    setInput('');

    try {
      const { data: { session } } = await supabase.auth.getSession();
      
      // Send request to backend
      const response = await fetch(`${env.apiBaseUrl}/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${session?.access_token}`,
        },
        body: JSON.stringify({
          id: threadId,
          messages: [{ id: crypto.randomUUID(), role: 'user', parts: [{ type: 'text', text: userMessage }] }],
        }),
      });

      if (!response.ok) throw new Error('Stream failed');
      if (!response.body) throw new Error('No response body');

      // Create a placeholder for assistant message
      const assistantMessageId = crypto.randomUUID();
      setMessages(prev => [...prev, 
        { id: assistantMessageId, role: 'assistant', content: '', created_at: new Date().toISOString() }
      ]);

      // Read the stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantContent = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('0:')) {
            // Text delta - extract the quoted text
            const textMatch = line.match(/0:"([^"]*)"/);
            if (textMatch) {
              assistantContent += textMatch[1];
              setMessages(prev => 
                prev.map(m => m.id === assistantMessageId ? { ...m, content: assistantContent } : m)
              );
            }
          }
        }
      }

      // Reload messages from backend to ensure consistency
      await getMessages(threadId).then(setMessages);
      
    } catch (error) {
      console.error('Chat error:', error);
      alert('Failed to send message');
    } finally {
      setIsLoading(false);
    }
  };

  if (!threadId) return <div className="p-8">No chat selected</div>;

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto p-4">
      <div className="mb-4">
        <Link to="/" className="text-blue-600 hover:underline">&larr; Back to Chats</Link>
      </div>

      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {messages.map((m) => (
          <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <Card className={`max-w-[80%] ${m.role === 'user' ? 'bg-blue-100' : 'bg-gray-100'}`}>
              <CardContent className="p-3">
                <p className="text-sm font-bold mb-1">{m.role === 'user' ? 'You' : 'Copilot'}</p>
                <p className="whitespace-pre-wrap">{m.content}</p>
              </CardContent>
            </Card>
          </div>
        ))}
        {isLoading && (
          <div className="text-sm text-gray-500 italic">Copilot is typing...</div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about SEC filings..."
          className="flex-1 p-2 border rounded-md"
          disabled={isLoading}
        />
        <Button type="submit" disabled={isLoading}>
          Send
        </Button>
      </form>
    </div>
  );
}