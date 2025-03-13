import "../styles/ConsultasSidebar.css"

const ConsultasSidebar = () => {
  const consultas = ["CONSULTA 1", "CONSULTA 2", "CONSULTA 3", "CONSULTA 4", "CONSULTA 5", "CONSULTA 6"]

  return (
    <div className="consultas-container">
      {consultas.map((consulta, index) => (
        <button key={index} className="consulta-button">
          {consulta}
        </button>
      ))}
    </div>
  )
}

export default ConsultasSidebar

