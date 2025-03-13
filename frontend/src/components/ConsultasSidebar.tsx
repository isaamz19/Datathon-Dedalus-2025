import "../styles/ConsultasSidebar.css"
import { useState } from "react"
import { ChevronDown, ChevronUp } from "lucide-react"

const ConsultasSidebar = () => {
  // Estado para controlar si las consultas están expandidas o no
  const [isExpanded, setIsExpanded] = useState(true)

  // Función para alternar la expansión de las consultas
  const toggleExpansion = () => {
    setIsExpanded(!isExpanded)
  }

  const consultas = ["CONSULTA 1", "CONSULTA 2", "CONSULTA 3", "CONSULTA 4", "CONSULTA 5", "CONSULTA 6"]

  return (
    <div className="consultas-sidebar">
      <div className="consultas-header" onClick={toggleExpansion}>
        <h3>CONSULTAS</h3>
        {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </div>

      {isExpanded && (
        <div className="consultas-container">
          {consultas.map((consulta, index) => (
            <button key={index} className="consulta-button">
              {consulta}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default ConsultasSidebar

