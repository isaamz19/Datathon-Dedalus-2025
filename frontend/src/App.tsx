import { useState, useEffect } from "react"
import WelcomeScreen from "./components/WelcomeScreen"
import ChatInterface from "./components/ChatInterface"
import "./index.css"

// Tipos de temas disponibles
type Theme = "light" | "dark" | "colorblind"

function App() {
  const [theme, setTheme] = useState<Theme>("light")
  const [started, setStarted] = useState(false)

  // Efecto para aplicar el tema al documento
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme)
  }, [theme])

  // Función para cambiar entre temas
  const toggleTheme = (newTheme: Theme) => {
    setTheme(newTheme)
    localStorage.setItem("theme", newTheme)
  }

  // Función para iniciar la aplicación
  const handleStart = () => {
    setStarted(true)
  }

  return (
    <div className="app-container">
      {!started ? <WelcomeScreen onStart={handleStart} /> : <ChatInterface theme={theme} onThemeChange={toggleTheme} />}
    </div>
  )
}

export default App

