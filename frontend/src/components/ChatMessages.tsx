"use client"

import { useEffect, useRef, useState } from "react"
import { BarChart, Volume2 } from "lucide-react"
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
  const [botMessageCount, setBotMessageCount] = useState(0)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })

    // Contar mensajes del bot
    const botMessages = messages.filter((msg) => msg.isBot)
    setBotMessageCount(botMessages.length)

    // Encontrar el índice del último mensaje del bot
    const lastBotIndex = messages.reduce((acc, msg, index) => (msg.isBot ? index : acc), -1)
    setLastBotMessage(lastBotIndex)
  }, [messages])

  const handleSpeak = (text: string) => {
    if (text && "speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = "es-ES"
      window.speechSynthesis.speak(utterance)
    } else {
      alert("Tu navegador no soporta la síntesis de voz o el mensaje está vacío.")
    }
  }

  // Función para preservar formato de texto
  const formatText = (text: string) => {
    // Reemplazar saltos de línea con elementos <br />
    const lines = text.split("\n")

    return (
      <>
        {lines.map((line, i) => (
          <span key={i}>
            {line}
            {i < lines.length - 1 && <br />}
          </span>
        ))}
      </>
    )
  }

  return (
    <div className="messages-container">
      {messages.map((msg, index) => (
        <div key={index} className={`message-container ${msg.isBot ? "bot-container" : "user-container"}`}>
          <div className={`message ${msg.isBot ? "bot-message" : "user-message"}`}>
            {msg.isBot && (
              <div className="bot-icon">
                <div className="small-bot-icon-placeholder"></div>
              </div>
            )}
            <div className="message-content">
              {/* Usar la función formatText para preservar formato */}
              {formatText(msg.text)}

              {/* Mostrar el botón de estadísticas y el altavoz solo si es un mensaje del bot, 
                  es el último mensaje del bot, y no es el primer mensaje del bot */}
              {msg.isBot && index === lastBotMessage && botMessageCount > 1 && (
                <div className="message-buttons">
                  <button className="speaker-button" onClick={() => handleSpeak(msg.text)}>
                    <Volume2 size={20} />
                  </button>
                  <button className="stats-button" onClick={() => setShowStats(true)}>
                    <BarChart size={16} />
                    Ver estadísticas
                  </button>
                </div>
              )}
              {/* Mostrar solo el botón de altavoz si es el primer mensaje del bot y es el último mensaje del bot */}
              {msg.isBot && index === lastBotMessage && botMessageCount === 1 && (
                <div className="message-buttons">
                  <button className="speaker-button" onClick={() => handleSpeak(msg.text)}>
                    <Volume2 size={20} />
                  </button>
                </div>
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

