import type React from "react"
import { useState } from "react"
import { Mic } from "lucide-react"
import "../styles/ChatInput.css"

type ChatInputProps = {
  onSendMessage: (message: string) => void
  isLoading: boolean
}

const ChatInput = ({ onSendMessage, isLoading }: ChatInputProps) => {
  const [message, setMessage] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (message.trim() && !isLoading) {
      onSendMessage(message)
      setMessage("")
    }
  }

  return (
    <form className="chat-input-container" onSubmit={handleSubmit}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="ESCRIBE A DR. DIAGNOBOT"
        disabled={isLoading}
        className="chat-input"
      />
      <button type="button" className="mic-button" aria-label="Usar micrófono">
        <Mic />
      </button>
    </form>
  )
}

export default ChatInput

