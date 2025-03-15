"use client"

import { useEffect, useRef, useState } from "react"
import { BarChart } from "lucide-react"
import StatisticsDialog from "./StatisticsDialog"
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
  const [showStats, setShowStats] = useState(false)
  const [lastBotMessage, setLastBotMessage] = useState<number | null>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    const lastBotIndex = messages.reduce((acc, msg, index) => (msg.isBot ? index : acc), -1)
    setLastBotMessage(lastBotIndex)
  }, [messages])

  return (
    <div className="messages-container">
      {messages.map((msg, index) => (
        <div key={index}>
          <div className={`message ${msg.isBot ? "bot-message" : "user-message"}`}>
            {msg.isBot && (
              <div className="bot-icon">
                <div className="small-bot-icon-placeholder"></div>
              </div>
            )}
            <div className="message-content">
              {msg.text}
              {/* Mostrar el botón de estadísticas dentro del mensaje del bot */}
              {msg.isBot && index === lastBotMessage && (
                <button className="stats-button" onClick={() => setShowStats(true)}>
                  <BarChart size={16} />
                  Ver estadísticas
                </button>
              )}
            </div>
          </div>
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
      <StatisticsDialog isOpen={showStats} onClose={() => setShowStats(false)} />
    </div>
  )
}

export default ChatMessages

