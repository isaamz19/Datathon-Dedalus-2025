import "../styles/ConsultasSidebar.css"
import { useState } from "react"
import { Plus, ChevronDown, ChevronUp } from "lucide-react"

const ConsultasSidebar = () => {
  // Estado para controlar si las consultas están expandidas o no
  const [isExpanded, setIsExpanded] = useState(true)

  // Función para alternar la expansión de las consultas
  const toggleExpansion = () => {
    setIsExpanded(!isExpanded)
  }

  // const consultas = ["CONSULTA 1", "CONSULTA 2", "CONSULTA 3", "CONSULTA 4", "CONSULTA 5", "CONSULTA 6"]
  // Estado para almacenar las consultas dinámicamente
  const [consultas, setConsultas] = useState<string[]>([])
  
  const addConsulta = () => {
    const newConsultaNumber = consultas.length + 1;
    setConsultas((prevConsultas) => [
      ...prevConsultas,
      `CONSULTA ${newConsultaNumber}`,
    ])
  }

  return (
    <div className="consultas-sidebar">
      <div className="consultas-header" onClick={toggleExpansion}>
        <h3>CONSULTAS</h3>
        {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </div>

      {/* Botón para agregar nueva consulta */}
      <div className="add-consulta-button-container">
        <button className="add-consulta-button" onClick={addConsulta} 
        aria-label="Nueva consulta"
        title="Nueva consulta">
          <Plus size={20} />
        </button>
      </div>

      {isExpanded && (
        <div className="consultas-container">
          {consultas.slice().reverse().map((consulta, index) => (
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

