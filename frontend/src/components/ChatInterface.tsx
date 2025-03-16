import { useState } from "react"
import { Menu } from "lucide-react"
import ConsultasSidebar from "./ConsultasSidebar"
import ChatInput from "./ChatInput"
import ChatMessages from "./ChatMessages"
import ThemeToggle from "./ThemeToggle"
import "../styles/ChatInterface.css"

type Theme = "light" | "dark" | "colorblind" | "dyslexia"

type ChatInterfaceProps = {
  theme: Theme
  onThemeChange: (theme: Theme) => void
}

// URL base del backend
const API_BASE_URL = "http://localhost:5000"

const ChatInterface = ({ theme, onThemeChange }: ChatInterfaceProps) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [messages, setMessages] = useState<Array<{ text: string; isBot: boolean }>>([
    { text: "Buenas, ¿en qué puedo ayudarte hoy?", isBot: true },
  ])
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return

    // Añadir mensaje del usuario a la interfaz
    const userMessage = { text, isBot: false }
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Primera llamada: enviar la pregunta del usuario
      const sendResponse = await fetch(`${API_BASE_URL}/api/send-question`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }),
      })

      if (!sendResponse.ok) {
        const errorData = await sendResponse.json()
        throw new Error(errorData.error || "Error al enviar la pregunta")
      }

      // Segunda llamada: obtener la respuesta del bot
      const getResponse = await fetch(`${API_BASE_URL}/api/get-bot-response`, {
        method: "GET",
      })

      if (!getResponse.ok) {
        const errorData = await getResponse.json()
        throw new Error(errorData.error || "Error al obtener la respuesta del bot")
      }

      const data = await getResponse.json()

      // Añadir respuesta del bot
      const botResponse = {
        text: data.message || "Lo siento, no pude procesar tu mensaje.",
        isBot: true,
      }

      setMessages((prev) => [...prev, botResponse])
    } catch (error) {
      console.error("Error en la comunicación con el backend:", error)
      setMessages((prev) => [
        ...prev,
        {
          text: "Lo siento, ha ocurrido un error. Inténtalo de nuevo más tarde.",
          isBot: true,
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-interface">
      <header className="app-header">
        <div className="header-content">
          <div className="header-left">
            <button className="menu-button" onClick={() => setSidebarOpen(!sidebarOpen)} aria-label="Toggle menu">
              <Menu />
            </button>
            <h1>DR. DIAGNOBOT</h1>
          </div>
          <div className="bot-logo">
            <div className="bot-logo-placeholder"></div>
          </div>
        </div>
      </header>

      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <ThemeToggle currentTheme={theme} onThemeChange={onThemeChange} />
        </div>
        <ConsultasSidebar />
      </aside>

      <main className={`main-content ${!sidebarOpen ? "expanded" : ""}`}>
        <div className="chat-container">
          <div className="messages-wrapper">
            <ChatMessages messages={messages} isLoading={isLoading} theme={theme} />
          </div>
          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
      </main>
    </div>
  )
}

export default ChatInterface

