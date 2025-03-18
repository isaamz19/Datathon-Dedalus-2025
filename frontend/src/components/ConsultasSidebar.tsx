"use client"

import { useState } from "react"
import { ChevronDown, ChevronUp } from "lucide-react"
import "../styles/ConsultasSidebar.css"

type TableSection = {
  title: string
  color: string
  fields: string[]
}

const ConsultasSidebar = () => {
  const [expandedSection, setExpandedSection] = useState<string | null>("pacientes")

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
              style={{ backgroundColor: section.color }}
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

