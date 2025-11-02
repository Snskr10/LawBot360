import './ChatMessage.css';

type ChatMessageProps = {
  message: {
    id: string;
    type: 'user' | 'ai';
    text: string;
    timestamp: Date;
    refs?: string[];
  };
  loading?: boolean;
};

export default function ChatMessage({ message, loading }: ChatMessageProps) {
  return (
    <div className={`chat-message ${message.type === 'user' ? 'chat-message-user' : 'chat-message-ai'}`}>
      {message.type === 'ai' && (
        <div className="chat-message-icon">
          <div className="ai-icon">🧠</div>
        </div>
      )}
      <div className="chat-message-content">
        <div className="chat-message-text">
          {loading ? (
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          ) : (
            <p>{message.text}</p>
          )}
        </div>
        {message.refs && message.refs.length > 0 && (
          <div className="chat-message-refs">
            <strong>References:</strong>
            <ul>
              {message.refs.map((ref, idx) => (
                <li key={idx}>{ref}</li>
              ))}
            </ul>
          </div>
        )}
        {message.type === 'user' && (
          <div className="chat-message-time">
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        )}
      </div>
    </div>
  );
}

