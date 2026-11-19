import type { GenerateResponse } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

/** Error with a user-facing message, thrown by API calls. */
export class ApiError extends Error {
  readonly status: number | null;

  constructor(message: string, status: number | null = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function generateCode(query: string): Promise<GenerateResponse> {
  let res: Response;
  try {
    res = await fetch(`${API_BASE}/api/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
  } catch {
    throw new ApiError("Failed to connect to the server.");
  }

  if (res.status === 429) {
    throw new ApiError("Rate limit exceeded. Please wait a moment and try again.", 429);
  }

  if (!res.ok) {
    const detail = await res.json().catch(() => null);
    throw new ApiError(detail?.detail ?? `Error: ${res.status}`, res.status);
  }

  try {
    return (await res.json()) as GenerateResponse;
  } catch {
    throw new ApiError("Failed to connect to the server.", res.status);
  }
}
