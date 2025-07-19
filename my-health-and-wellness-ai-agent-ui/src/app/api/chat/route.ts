import type { NextRequest } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { query } = await request.json()

    if (!query) {
      return new Response("Query is required", { status: 400 })
    }

    // Make request to your FastAPI backend
    const response = await fetch("https://q4-assignments-and-projects.vercel.app/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    })

    if (!response.ok) {
      throw new Error(`FastAPI responded with status: ${response.status}`)
    }

    // Return the streaming response from FastAPI
    return new Response(response.body, {
      headers: {
        "Content-Type": "text/plain",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      },
    })
  } catch (error) {
    console.error("Error in API route:", error)
    return new Response("Internal Server Error", { status: 500 })
  }
}
