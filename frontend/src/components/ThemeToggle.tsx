import { Moon, Sun, Eye, BookOpen} from "lucide-react"
import "../styles/ThemeToggle.css"

type ThemeToggleProps = {
  currentTheme: "light" | "dark" | "colorblind" | "dyslexia"
  onThemeChange: (theme: "light" | "dark" | "colorblind"| "dyslexia") => void
}

const ThemeToggle = ({ currentTheme, onThemeChange }: { currentTheme: string; onThemeChange: (theme: string) => void }) => {
  const isLightMode = currentTheme === "light";  
  
  return (
    <div className="theme-toggle">
      <button
      className="theme-button"
      onClick={() => onThemeChange(isLightMode ? "dark" : "light")}
      aria-label={isLightMode ? "Modo noche" : "Modo día"}
      title={isLightMode ? "Modo noche" : "Modo día"}
    >
      {isLightMode ? <Moon size={20} /> : <Sun size={20} />}
    </button>
      <button
        className={`theme-button ${currentTheme === "colorblind" ? "active" : ""}`}
        onClick={() => onThemeChange("colorblind")}
        aria-label="Modo daltonismo"
        title="Modo daltonismo"
      >
        <Eye size={20} />
      </button>
      <button
        className={`theme-button ${currentTheme === "dyslexia" ? "active" : ""}`}
        onClick={() => onThemeChange("dyslexia")}
        aria-label="Modo dislexia"
        title="Modo dislexia"
      >
        <BookOpen size={20} />
      </button>
    </div>
  )
}

export default ThemeToggle

