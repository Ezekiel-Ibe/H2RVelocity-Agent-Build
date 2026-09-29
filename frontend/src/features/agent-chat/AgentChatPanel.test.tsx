import { useState } from "react";
import { describe, it, expect } from "vitest";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { AgentChatPanel as RealAgentChatPanel } from "./AgentChatPanel";
import { renderWithProviders } from "@/test/renderWithProviders";
import { initialChatMessages } from "@/fixtures/dashboard";
import type { ChatMessage } from "@/contracts/schemas";

// Harness supplies the conversation state the panel now receives from App.
function AgentChatPanel() {
  const [messages, setMessages] = useState<ChatMessage[]>(initialChatMessages);
  const [conversationId, setConversationId] = useState<string | null>(null);
  return (
    <RealAgentChatPanel
      messages={messages}
      setMessages={setMessages}
      conversationId={conversationId}
      setConversationId={setConversationId}
    />
  );
}

describe("AgentChatPanel", () => {
  it("renders the agent chat landmark and disclaimer", () => {
    renderWithProviders(<AgentChatPanel />);
    expect(screen.getByRole("complementary", { name: "Agent chat" })).toBeInTheDocument();
    expect(
      screen.getByText(/Agent responses may contain inaccuracies/i),
    ).toBeInTheDocument();
  });

  it("shows suggested prompts initially", () => {
    renderWithProviders(<AgentChatPanel />);
    expect(
      screen.getByRole("button", { name: /Summarize current open cases/i }),
    ).toBeInTheDocument();
  });

  it("adds the user message when a prompt is sent", async () => {
    const user = userEvent.setup();
    renderWithProviders(<AgentChatPanel />);
    const input = screen.getByLabelText(/Ask the agent anything/i);
    await user.type(input, "Show me overtime exceptions");
    await user.click(screen.getByRole("button", { name: /Send message/i }));
    await waitFor(() =>
      expect(screen.getByText(/Show me overtime exceptions/i)).toBeInTheDocument(),
    );
  });

  it("shows an agent reply from the mock API", async () => {
    const user = userEvent.setup();
    renderWithProviders(<AgentChatPanel />);
    await user.click(
      screen.getByRole("button", { name: /Summarize current open cases/i }),
    );
    await waitFor(() =>
      expect(screen.getByText(/Development response:/i)).toBeInTheDocument(),
    );
    expect(screen.getByText("Evidence:")).toBeInTheDocument();
    expect(screen.getByText("EV-01")).toBeInTheDocument();
  });

  it("returns INSUFFICIENT_EVIDENCE when grounding is missing", async () => {
    const user = userEvent.setup();
    renderWithProviders(<AgentChatPanel />);
    const input = screen.getByLabelText(/Ask the agent anything/i);
    await user.type(input, "Can you forecast next month's payroll errors?");
    await user.click(screen.getByRole("button", { name: /Send message/i }));
    await waitFor(() =>
      expect(screen.getByText("Insufficient evidence")).toBeInTheDocument(),
    );
    expect(screen.getByText(/INSUFFICIENT_EVIDENCE/)).toBeInTheDocument();
  });
});
