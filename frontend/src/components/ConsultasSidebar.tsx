"use client"

import { useState, useEffect } from "react"
import { ChevronDown, ChevronUp } from "lucide-react"
import "../styles/ConsultasSidebar.css"

type TableSection = {
  title: string
  color: string
  fields: string[]
}

const ConsultasSidebar = () => {
  const [expandedSection, setExpandedSection] = useState<string | null>("pacientes")
  const [theme, setTheme] = useState<string>("light")

  // Detectar cambios en el tema
  useEffect(() => {
    const currentTheme = document.documentElement.getAttribute("data-theme") || "light"
    setTheme(currentTheme)

    // Observar cambios en el atributo data-theme
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === "attributes" && mutation.attributeName === "data-theme") {
          setTheme(document.documentElement.getAttribute("data-theme") || "light")
        }
      })
    })

    observer.observe(document.documentElement, { attributes: true })

    return () => observer.disconnect()
  }, [])

  // Función para obtener colores adaptados al tema
  const getThemeColor = (baseColor: string): string => {
    switch (theme) {
      case "dark":
        // Colores más claros para el tema oscuro
        return (
          {
            "#FF914D": "#FFA76B", // Naranja más claro
            "#B8D2AD": "#D8F0CC", // Verde más claro
            "#9FAD86": "#BFCCa8", // Verde oliva más claro
            "#CFBDAA": "#E0D0C0", // Beige más claro
            "#EAE2DA": "#F5F0EB", // Crema más claro
            "#FFB347": "#FFC675", // Naranja amarillento más claro
            "#A2CDB0": "#C2EDD0", // Verde menta más claro
          }[baseColor] || baseColor
        )
      case "colorblind":
        // Colores para daltonismo
        return (
          {
            "#FF914D": "#dde5b6", // Azul oscuro
            "#B8D2AD": "#dde5b6", // Verde azulado
            "#9FAD86": "#dde5b6", // Amarillo
            "#CFBDAA": "#dde5b6", // Naranja
            "#EAE2DA": "#dde5b6", // Rojo anaranjado
            "#FFB347": "#dde5b6", // Azul muy oscuro
            "#A2CDB0": "#dde5b6", // Azul medio
          }[baseColor] || baseColor
        )
      case "dyslexia":
        // Colores para dislexia (alto contraste)
        return (
          {
            "#FF914D": "#ffffff", // Azul oscuro
            "#B8D2AD": "#ffffff", // Azul medio
            "#9FAD86": "#ffffff", // Azul claro
            "#CFBDAA": "#ffffff", // Blanco roto
            "#EAE2DA": "#ffffff", // Rojo
            "#FFB347": "#ffffff", // Azul oscuro
            "#A2CDB0": "#ffffff", // Azul claro
          }[baseColor] || baseColor
        )
      default:
        return baseColor
    }
  }

  const tableSections: TableSection[] = [
    {
      title: "Pacientes",
      color: "#FF914D",
      fields: ["Fecha de nacimiento", "Raza", "Fecha de muerte", "Edad", "Provincia", "Género"],
    },
    {
      title: "Medicaciones",
      color: "#B8D2AD",
      fields: [
        "Fecha de inicio",
        "Fecha de fin",
        "Código del medicamento",
        "Frecuencia",
        "Vía de administración",
        "Descripción/Nombre",
      ],
    },
    {
      title: "Condiciones",
      color: "#9FAD86",
      fields: ["Descripción de la condición", "Código de la condición", "Fecha de inicio", "Fecha de fin"],
    },
    {
      title: "Encuentros",
      color: "#CFBDAA",
      fields: [
        "Fecha de inicio",
        "Fecha de fin",
        "Tipo de encuentro",
        "Razón del encuentro",
        "Descripción del encuentro",
      ],
    },
    {
      title: "Procedimientos",
      color: "#EAE2DA",
      fields: ["Razón del procedimiento", "Descripción del procedimiento", "Código del procedimiento"],
    },
    {
      title: "Inmunizaciones",
      color: "#FFB347",
      fields: ["Código de vacunación", "Descripción de la vacunación"],
    },
    {
      title: "Alergias",
      color: "#A2CDB0",
      fields: ["Descripción de la alergia", "Código de la alergia"],
    },
  ]

  const toggleSection = (title: string) => {
    setExpandedSection(expandedSection === title ? null : title)
  }

  return (
    <div className="sidebar-content">
      <h2 className="sidebar-title">Campos Disponibles</h2>
      <div className="table-sections">
        {tableSections.map((section) => (
          <div key={section.title} className="table-section">
            <button
              className="section-header"
              onClick={() => toggleSection(section.title)}
              style={{ backgroundColor: getThemeColor(section.color) }}
            >
              <span>{section.title}</span>
              {expandedSection === section.title ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
            </button>
            {expandedSection === section.title && (
              <div className="section-content">
                <ul className="fields-list">
                  {section.fields.map((field) => (
                    <li key={field} className="field-item">
                      {field}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ConsultasSidebar