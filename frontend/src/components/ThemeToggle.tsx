"use client"

import { Moon, Sun, Eye } from "lucide-react"
import "../styles/ThemeToggle.css"

type ThemeToggleProps = {
  currentTheme: "light" | "dark" | "colorblind"
  onThemeChange: (theme: "light" | "dark" | "colorblind") => void
}

const ThemeToggle = ({ currentTheme, onThemeChange }: ThemeToggleProps) => {
  return (
    <div className="theme-toggle">
      <button
        className={`theme-button ${currentTheme === "light" ? "active" : ""}`}
        onClick={() => onThemeChange("light")}
        aria-label="Modo día"
        title="Modo día"
      >
        <Sun size={20} />
      </button>
      <button
        className={`theme-button ${currentTheme === "dark" ? "active" : ""}`}
        onClick={() => onThemeChange("dark")}
        aria-label="Modo noche"
        title="Modo noche"
      >
        <Moon size={20} />
      </button>
      <button
        className={`theme-button ${currentTheme === "colorblind" ? "active" : ""}`}
        onClick={() => onThemeChange("colorblind")}
        aria-label="Modo daltónico"
        title="Modo daltónico"
      >
        <Eye size={20} />
      </button>
    </div>
  )
}

export default ThemeToggle

