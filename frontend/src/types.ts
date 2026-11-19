export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface RetrievedFunction {
  score: number;
  function_name: string;
  parameters: string[];
  code: string;
}

export interface GenerateResponse {
  generated_code: string | null;
  retrieved_functions: RetrievedFunction[];
  cached: boolean;
}
