import { useState } from "react"
import { Moon, Sun, Eye, Search, Menu } from "lucide-react"
import ConsultasSidebar from "./ConsultasSidebar"
import ChatInput from "./ChatInput"
import ChatMessages from "./ChatMessages"
import "../styles/ChatInterface.css"

type Theme = "light" | "dark" | "colorblind"

type ChatInterfaceProps = {
  theme: Theme
  onThemeChange: (theme: Theme) => void
}

const ChatInterface = ({ theme, onThemeChange }: ChatInterfaceProps) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [messages, setMessages] = useState<Array<{ text: string; isBot: boolean }>>([
    { text: "¿EN QUÉ PUEDO AYUDARTE?", isBot: true },
  ])
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return

    // Añadir mensaje del usuario
    const userMessage = { text, isBot: false }
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Simulación de respuesta del bot
      setTimeout(() => {
        const botResponse = {
          text: `¡Claro! Aquí tienes la información sobre: "${text}"`,
          isBot: true,
        }
        setMessages((prev) => [...prev, botResponse])
        setIsLoading(false)
      }, 1000)
    } catch (error) {
      console.error("Error al enviar mensaje:", error)
      setMessages((prev) => [
        ...prev,
        {
          text: "Lo siento, ha ocurrido un error. Inténtalo de nuevo más tarde.",
          isBot: true,
        },
      ])
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-interface">
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="theme-controls">
          <div className="theme-toggle">
            <button
              className={`theme-button ${theme === "light" ? "active" : ""}`}
              onClick={() => onThemeChange("light")}
              aria-label="Modo día"
              title="Modo día"
            >
              <Sun size={20} />
            </button>
            <button
              className={`theme-button ${theme === "dark" ? "active" : ""}`}
              onClick={() => onThemeChange("dark")}
              aria-label="Modo noche"
              title="Modo noche"
            >
              <Moon size={20} />
            </button>
            <button
              className={`theme-button ${theme === "colorblind" ? "active" : ""}`}
              onClick={() => onThemeChange("colorblind")}
              aria-label="Modo daltónico"
              title="Modo daltónico"
            >
              <Eye size={20} />
            </button>
          </div>
          <button className="search-button" aria-label="Buscar">
            <Search />
          </button>
        </div>
        <ConsultasSidebar />
      </aside>

      <main className="main-content">
        <button className="menu-toggle" onClick={() => setSidebarOpen(!sidebarOpen)} aria-label="Abrir menú">
          <Menu />
        </button>

        <div className="chat-container">
          <div className="bot-header">
            <h1>HOLA, SOY EL DR. DIAGNOBOT</h1>
            <div className="bot-avatar">
              <div className="bot-logo-placeholder"></div>
            </div>
          </div>

          <ChatMessages messages={messages} isLoading={isLoading} theme={theme} />

          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
      </main>
    </div>
  )
}

export default ChatInterface

