import { useEffect, useRef } from "react"
import "../styles/ChatMessages.css"

type Message = {
  text: string
  isBot: boolean
}

type ChatMessagesProps = {
  messages: Message[]
  isLoading: boolean
  theme: string
}

const ChatMessages = ({ messages, isLoading }: ChatMessagesProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Scroll al final cuando hay nuevos mensajes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  return (
    <div className="messages-container">
      {messages.map((msg, index) => (
        <div key={index} className={`message ${msg.isBot ? "bot-message" : "user-message"}`}>
          {msg.isBot && (
            <div className="bot-icon">
              <div className="small-bot-icon-placeholder"></div>
            </div>
          )}
          <div className="message-content">{msg.text}</div>
        </div>
      ))}
      {isLoading && (
        <div className="message bot-message">
          <div className="bot-icon">
            <div className="small-bot-icon-placeholder"></div>
          </div>
          <div className="message-content typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  )
}

export default ChatMessages

