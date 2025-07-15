// app/page.tsx
"use client";

import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const apiUrl = 'https://q4-assignments-and-projects-k9b3.vercel.app'; // Replace with your actual API URL

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setResponse(''); // Clear previous response

    try {
      const res = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      // Check if the response body is available
      if (!res.body) {
        throw new Error("Response body is null.");
      }
      
      // Use a TextDecoder to decode the stream chunks
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          break; // The stream has finished
        }
        // Decode the chunk and append it to the response state
        const chunk = decoder.decode(value, { stream: true });
        setResponse((prev) => prev + chunk);
      }

    } catch (error) {
      console.error("Failed to fetch stream:", error);
      setResponse("An error occurred while fetching the response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-gray-50">
      <div className="w-full max-w-2xl">
        <h1 className="text-4xl font-bold mb-6 text-center text-gray-800">
          Health & Wellness Agent
        </h1>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-md mb-4 text-black focus:ring-2 focus:ring-blue-500"
              placeholder="Ask your health and wellness question..."
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white p-3 rounded-md hover:bg-blue-700 disabled:bg-blue-300"
            >
              {loading ? 'Thinking...' : 'Ask'}
            </button>
          </form>
          {response && (
            <div className="mt-6 p-4 bg-gray-100 rounded-md text-gray-700 whitespace-pre-wrap">
              <p>{response}</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}