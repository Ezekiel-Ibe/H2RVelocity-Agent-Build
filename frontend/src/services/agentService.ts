import { agentResponseSchema, type AgentResponse } from "@/contracts/schemas";
import { API_BASE_URL } from "./apiConfig";
import { endpoints } from "./endpoints";

export async function sendAgentMessage(
  prompt: string,
  conversationId?: string | null,
): Promise<AgentResponse> {
  const response = await fetch(`${API_BASE_URL}${endpoints.agentMessages}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, conversationId }),
  });
  if (!response.ok) {
    throw new Error(`Failed to send message (${response.status})`);
  }
  const payload: unknown = await response.json();
  return agentResponseSchema.parse(payload);
}

export type AgentStreamHandlers = {
  onStatus: (text: string) => void;
  onDelta: (text: string) => void;
  onDone: (conversationId: string | null) => void;
};

/**
 * Stream an agent turn over SSE. The orchestrator's "Asking the A05 agent…"
 * narration arrives first as `status` events; the answer follows as `delta`
 * events; then `done` with the conversation id. Throws on transport or server
 * error so the caller can fall back to the non-streaming endpoint.
 */
export async function streamAgentMessage(
  prompt: string,
  conversationId: string | null | undefined,
  handlers: AgentStreamHandlers,
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}${endpoints.agentStream}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, conversationId }),
  });
  if (!response.ok || !response.body) {
    throw new Error(`Failed to stream message (${response.status})`);
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const chunks = buffer.split("\n\n");
    buffer = chunks.pop() ?? "";
    for (const chunk of chunks) {
      const dataLine = chunk.split("\n").find((l) => l.startsWith("data:"));
      if (!dataLine) continue;
      const json = dataLine.slice("data:".length).trim();
      if (!json) continue;
      let evt: { type?: string; text?: string; conversationId?: string | null; message?: string };
      try {
        evt = JSON.parse(json);
      } catch {
        continue;
      }
      if (evt.type === "status" && evt.text) handlers.onStatus(evt.text);
      else if (evt.type === "delta" && evt.text) handlers.onDelta(evt.text);
      else if (evt.type === "done") handlers.onDone(evt.conversationId ?? null);
      else if (evt.type === "error") throw new Error(evt.message ?? "stream error");
    }
  }
}

/** Remove an immediately-repeated leading segment — the orchestrator emits its
 *  narration once, then repeats it verbatim at the start of the answer. Safe:
 *  returns the input unchanged if no clear duplicate is found (never blanks). */
export function dedupeLeadingRepeat(text: string): string {
  const t = text.replace(/^\s+/, "");
  const max = Math.min(400, Math.floor(t.length / 2));
  for (let i = max; i >= 12; i--) {
    const first = t.slice(0, i).trim();
    const after = t.slice(i).replace(/^\s+/, "");
    if (first.length >= 12 && after.startsWith(first)) {
      return after; // drop the first (duplicated) copy, keep the copy + answer
    }
  }
  return text;
}

/** Collapse consecutive paragraphs where one repeats or extends the previous —
 *  covers the non-streaming fallback where narration is concatenated. */
export function collapseRepeatedParagraphs(text: string): string {
  const paras = text.split(/\n{2,}/);
  const out: string[] = [];
  for (const p of paras) {
    const prev = out[out.length - 1];
    if (out.length && (prev.trim() === p.trim() || p.trim().startsWith(prev.trim()))) {
      out[out.length - 1] = p; // keep the fuller paragraph, drop the bare narration
    } else {
      out.push(p);
    }
  }
  return out.join("\n\n");
}
