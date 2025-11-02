import { useState, useRef, useEffect } from 'react';
import { sendChatMessage, ChatMessage } from '../api/client';
import Sidebar from '../components/Sidebar';
import ChatMessageComponent from '../components/ChatMessage';
import ExampleQuestions from '../components/ExampleQuestions';
import './ChatPage.css';

const exampleQuestions = [
  "Someone's pet dog bit me, what can I do?",
  "Someone is repeatedly calling me and harassing me, what can I do?",
  "How do I file a case against a person who has not returned my money after I lent it to them?",
  "What are the steps I can take towards filing for divorce?"
];

const welcomeMessage = "Hello, I am an AI-powered bot that can answer your legal queries related to Indian Laws and give you answers relevant to your questions. I am not a legal advisor or lawyer. Please consult a lawyer with your query to find a solution for your legal issues. I can only provide a starting ground so you understand your rights better and get more information regarding your questions before consulting a lawyer.";

type Message = {
  id: string;
  type: 'user' | 'ai';
  text: string;
  timestamp: Date;
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'ai',
      text: welcomeMessage,
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [showExamples, setShowExamples] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      text: text.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);
    setShowExamples(false);

    try {
      // Convert messages to ChatGPT format (excluding welcome message)
      const chatHistory: ChatMessage[] = messages
        .filter(msg => msg.id !== '1') // Exclude welcome message
        .map(msg => ({
          role: msg.type === 'user' ? 'user' : 'assistant',
          content: msg.text
        }));

      const response = await sendChatMessage(chatHistory, text.trim());

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        text: response.message || 'I apologize, but I could not generate a response. Please try again.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error: any) {
      console.error('Chat error:', error);
      let errorMessage = 'I apologize, but I encountered an error processing your question. ';
      
      if (error?.response?.status === 503) {
        errorMessage = error.response.data?.error || 'OpenAI API is not configured. Please set OPENAI_API_KEY in your environment variables.';
      } else if (error?.response?.status === 0 || error?.code === 'ERR_NETWORK' || error?.code === 'ECONNREFUSED') {
        errorMessage += 'Please ensure the backend server is running on port 5000.';
      } else if (error?.response?.data?.error) {
        errorMessage += error.response.data.error;
      } else if (error?.message) {
        errorMessage += error.message;
      } else {
        errorMessage += 'Please try again or rephrase your question.';
      }
      
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        text: errorMessage,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSendMessage(inputValue);
  };

  const handleExampleClick = (question: string) => {
    handleSendMessage(question);
  };

  return (
    <div className="chat-page">
      <Sidebar />
      <div className="chat-main">
        {/* Announcement Banner */}
        <div className="announcement-banner">
          <span className="announcement-icon">⚠️</span>
          <span className="announcement-text">
            Draft legal documents? Check out our latest AI-powered drafting + research application! 
            Visit <a href="https://draftbotpro.com" target="_blank" rel="noopener noreferrer">draftbotpro.com</a> now!
          </span>
        </div>

        {/* Chat Messages */}
        <div className="chat-messages-container">
          {messages.map((message) => (
            <ChatMessageComponent key={message.id} message={message} />
          ))}
          
          {loading && (
            <ChatMessageComponent
              message={{
                id: 'loading',
                type: 'ai',
                text: 'Thinking...',
                timestamp: new Date(),
              }}
              loading={true}
            />
          )}
          
          {showExamples && messages.length === 1 && (
            <ExampleQuestions
              questions={exampleQuestions}
              onQuestionClick={handleExampleClick}
            />
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Chat Input */}
        <form className="chat-input-container" onSubmit={handleSubmit}>
          <input
            ref={inputRef}
            type="text"
            className="chat-input"
            placeholder="Send a message.."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={loading}
          />
          <button
            type="submit"
            className="chat-send-button"
            disabled={loading || !inputValue.trim()}
          >
            Send
          </button>
        </form>

        {/* Footer Disclaimer */}
        <div className="chat-footer">
          <p>
            LawBot 360 has been designed with help from Giri & Co., a 40 year old law firm based in New Delhi, India, 
            specialising in all sorts of civil and criminal matters.{' '}
            <a href="#" onClick={(e) => { e.preventDefault(); window.open('https://giriandco.com', '_blank'); }}>
              Giri & Co.
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
