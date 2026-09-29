import { useRef, useState, type Dispatch, type SetStateAction } from "react";
import {
  SparkleRegular,
  OpenRegular,
  MoreHorizontalRegular,
  SendRegular,
  AddRegular,
  PanelRightContractRegular,
  WarningRegular,
} from "@fluentui/react-icons";
import type { ChatMessage } from "@/contracts/schemas";
import { initialChatMessages, suggestedPrompts } from "@/fixtures/dashboard";
import {
  sendAgentMessage,
  streamAgentMessage,
  collapseRepeatedParagraphs,
  dedupeLeadingRepeat,
} from "@/services/agentService";
import { USE_MOCKS } from "@/services/apiConfig";
import { MessageContent } from "./MessageContent";
import styles from "./AgentChatPanel.module.css";

type AgentChatPanelProps = {
  messages: ChatMessage[];
  setMessages: Dispatch<SetStateAction<ChatMessage[]>>;
  conversationId: string | null;
  setConversationId: Dispatch<SetStateAction<string | null>>;
  onClose?: () => void;
  onResizeStart?: (event: React.PointerEvent) => void;
  onResizeReset?: () => void;
};

export function AgentChatPanel({
  messages,
  setMessages,
  conversationId,
  setConversationId,
  onClose,
  onResizeStart,
  onResizeReset,
}: AgentChatPanelProps) {
  const [draft, setDraft] = useState("");
  const [thinking, setThinking] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const liveRef = useRef<HTMLDivElement>(null);

  async function send(text: string) {
    const trimmed = text.trim();
    if (!trimmed || thinking) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      author: "user",
      body: trimmed,
      timestamp: "Just now",
      status: "complete",
    };
    setMessages((prev) => [...prev, userMessage]);
    setDraft("");
    setThinking(true);

    // Non-streaming fallback: single POST that also retries server-side on a
    // transient Fabric throttle. Used for mocks and if streaming is unavailable.
    async function sendBlocking() {
      const reply = await sendAgentMessage(trimmed, conversationId);
      if (reply.conversationId) setConversationId(reply.conversationId);
      setNotice(reply.notice ?? null);
      setMessages((prev) => [
        ...prev,
        {
          ...reply,
          status: "complete",
          citations: reply.citations,
          evidenceStatus: reply.evidenceStatus,
        },
      ]);
      if (liveRef.current) liveRef.current.textContent = "Agent responded.";
    }

    try {
      if (USE_MOCKS) {
        await sendBlocking();
        return;
      }
      // Stream the turn into a SINGLE body so it can never blank out. The
      // orchestrator's narration arrives first, then the answer; the repeated
      // narration is de-duplicated at render time.
      const agentId = `agent-${Date.now()}`;
      let acc = "";
      let started = false;
      const transientFail = /data query failed|couldn.t retrieve|could not retrieve/i;

      const append = (text: string) => {
        acc += text;
        if (!started) {
          started = true;
          setThinking(false);
          setMessages((prev) => [
            ...prev,
            {
              id: agentId,
              author: "agent",
              body: acc,
              timestamp: "Just now",
              status: "streaming",
            },
          ]);
        } else {
          setMessages((prev) =>
            prev.map((m) => (m.id === agentId ? { ...m, body: acc } : m)),
          );
        }
      };

      try {
        await streamAgentMessage(trimmed, conversationId, {
          onStatus: append,
          onDelta: append,
          onDone: (cid) => {
            if (cid) setConversationId(cid);
          },
        });
      } catch {
        // Streaming failed before any token — fall back to the blocking path.
        if (!started) {
          await sendBlocking();
          return;
        }
        throw new Error("stream interrupted");
      }

      // A transient throttle failure (or empty stream) → re-ask via the blocking
      // endpoint, which retries server-side, and replace the placeholder.
      if (!acc.trim() || transientFail.test(acc)) {
        setMessages((prev) => prev.filter((m) => m.id !== agentId));
        await sendBlocking();
        return;
      }
      setMessages((prev) =>
        prev.map((m) =>
          m.id === agentId
            ? { ...m, body: acc, status: "complete", evidenceStatus: "grounded" }
            : m,
        ),
      );
      if (liveRef.current) liveRef.current.textContent = "Agent responded.";
    } catch {
      setNotice("Foundry agent is not reachable. Check the BFF and your Azure sign-in.");
      setMessages((prev) => [
        ...prev,
        {
          id: `agent-error-${Date.now()}`,
          author: "agent",
          body: "Sorry, the agent is unavailable right now. Please try again.",
          timestamp: "Just now",
          status: "complete",
        },
      ]);
      if (liveRef.current) liveRef.current.textContent = "Agent request failed.";
    } finally {
      setThinking(false);
    }
  }

  function newChat() {
    setMessages(initialChatMessages);
    setDraft("");
    setThinking(false);
    setNotice(null);
    setConversationId(null);
  }

  return (
    <aside className={styles.panel} aria-label="Agent chat">
      {onResizeStart && (
        <div
          className={styles.resizer}
          role="separator"
          aria-orientation="vertical"
          aria-label="Resize agent chat panel"
          onPointerDown={onResizeStart}
          onDoubleClick={onResizeReset}
        />
      )}
      <header className={styles.header}>
        <div className={styles.headerTitle}>
          <SparkleRegular aria-hidden="true" className={styles.sparkle} />
          <span>Agent Chat</span>
        </div>
        <div className={styles.headerActions}>
          <button type="button" className={styles.iconButton} aria-label="Open in new window">
            <OpenRegular />
          </button>
          <button type="button" className={styles.iconButton} aria-label="More options">
            <MoreHorizontalRegular />
          </button>
          {onClose && (
            <button
              type="button"
              className={styles.iconButton}
              aria-label="Collapse agent chat"
              onClick={onClose}
            >
              <PanelRightContractRegular />
            </button>
          )}
        </div>
      </header>

      <div className={styles.identity}>
        <SparkleRegular aria-hidden="true" className={styles.sparkleSmall} />
        <span className={styles.identityName}>Payroll Assurance Agent</span>
        <span className={styles.badge}>KPMG</span>
        <span className={styles.aiStatus}>
          <span className={styles.statusDot} aria-hidden="true" />
          AI
        </span>
      </div>

      {notice && (
        <div className={styles.notice} role="alert">
          <WarningRegular aria-hidden="true" className={styles.noticeIcon} />
          <span>{notice}</span>
        </div>
      )}

      <div className={styles.conversation}>
        {messages.map((msg) =>
          msg.author === "agent" ? (
            <div key={msg.id} className={styles.agentTurn}>
              <div className={styles.agentLabel}>
                <SparkleRegular aria-hidden="true" className={styles.sparkleSmall} />
                Payroll Assurance Agent
                <span className={styles.badge}>KPMG</span>
              </div>
              <div
                className={styles.agentBubble}
                data-insufficient={msg.evidenceStatus === "insufficient_evidence"}
              >
                {msg.evidenceStatus === "insufficient_evidence" && (
                  <span className={styles.insufficientBadge}>Insufficient evidence</span>
                )}
                <MessageContent
                  body={collapseRepeatedParagraphs(dedupeLeadingRepeat(msg.body))}
                />
                {msg.status === "streaming" && (
                  <div className={styles.streamingRow} role="status" aria-live="polite">
                    <span className={styles.thinking}>Consulting agents…</span>
                    <span className={styles.dots} aria-hidden="true">
                      <span />
                      <span />
                      <span />
                    </span>
                  </div>
                )}
                {msg.citations && msg.citations.length > 0 && (
                  <p className={styles.citations}>
                    <span className={styles.citationsLabel}>Evidence:</span>
                    {msg.citations.map((c) => (
                      <span key={c} className={styles.citation}>
                        {c}
                      </span>
                    ))}
                  </p>
                )}
                <span className={styles.timestamp}>{msg.timestamp}</span>
              </div>
            </div>
          ) : (
            <div key={msg.id} className={styles.userTurn}>
              <div className={styles.userBubble}>{msg.body}</div>
              <span className={styles.userTimestamp}>You · {msg.timestamp}</span>
            </div>
          ),
        )}

        {messages.length <= 1 && (
          <div className={styles.prompts}>
            {suggestedPrompts.map((prompt) => (
              <button
                key={prompt}
                type="button"
                className={styles.promptChip}
                onClick={() => send(prompt)}
              >
                {prompt}
              </button>
            ))}
          </div>
        )}

        {thinking && (
          <div className={styles.agentTurn}>
            <div className={styles.agentLabel}>
              <SparkleRegular aria-hidden="true" className={styles.sparkleSmall} />
              Payroll Assurance Agent
              <span className={styles.badge}>KPMG</span>
            </div>
            <div className={styles.agentBubble}>
              <span className={styles.thinking}>Analyzing payroll data…</span>
              <span className={styles.dots} aria-hidden="true">
                <span />
                <span />
                <span />
              </span>
            </div>
          </div>
        )}

        <div ref={liveRef} className="pa-visually-hidden" aria-live="polite" role="status" />
      </div>

      <div className={styles.composerArea}>
        <div className={styles.composerHead}>
          <button type="button" className={styles.newChat} onClick={newChat}>
            <AddRegular aria-hidden="true" />
            New Chat
          </button>
        </div>
        <form
          className={styles.composer}
          onSubmit={(e) => {
            e.preventDefault();
            send(draft);
          }}
        >
          <label htmlFor="agent-input" className="pa-visually-hidden">
            Ask the agent anything
          </label>
          <input
            id="agent-input"
            className={styles.input}
            placeholder="Ask the agent anything…"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            autoComplete="off"
          />
          <button
            type="submit"
            className={styles.send}
            aria-label="Send message"
            disabled={!draft.trim() || thinking}
          >
            <SendRegular />
          </button>
        </form>
        <p className={styles.disclaimer}>
          Agent responses may contain inaccuracies. Please validate important information.
        </p>
      </div>
    </aside>
  );
}
