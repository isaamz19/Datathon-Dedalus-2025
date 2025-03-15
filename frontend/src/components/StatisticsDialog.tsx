import { useEffect } from "react"
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts"
import { X } from "lucide-react"
import AndalusiaMap from "./AndalusiaMap"
import "../styles/StatisticsDialog.css"

const genderData = [
  { name: "Mujeres", value: 44 },
  { name: "Hombres", value: 56 },
]

const ageData = [
  { name: "< 18", value: 23 },
  { name: "18-25", value: 12 },
  { name: "25-40", value: 56 },
  { name: "40-70", value: 4 },
  { name: "> 70", value: 1 },
  { name: "Fallecidos", value: 4 },
]

const COLORS = ["#FF914D", "#B8D2AD"]

type StatisticsDialogProps = {
  isOpen: boolean
  onClose: () => void
}

const StatisticsDialog = ({ isOpen, onClose }: StatisticsDialogProps) => {
  // Prevenir scroll del body cuando el modal está abierto
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden"
    } else {
      document.body.style.overflow = "auto"
    }

    return () => {
      document.body.style.overflow = "auto"
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <>
      <div className="statistics-overlay" onClick={onClose}></div>
      <div className="statistics-dialog">
        <div className="statistics-header">
          ESTADÍSTICAS
          <button className="close-button" onClick={onClose}>
            <X size={24} />
          </button>
        </div>
        <div className="statistics-content">
          <div className="statistics-grid">
            {/* Género */}
            <div className="statistics-card">
              <h3>Distribución por Género</h3>
              <div className="chart-container">
                <PieChart width={300} height={300}>
                  <Pie
                    data={genderData}
                    cx={150}
                    cy={150}
                    innerRadius={60}
                    outerRadius={100}
                    fill="#8884d8"
                    paddingAngle={5}
                    dataKey="value"
                    label={({ name, value }) => `${name}: ${value}%`}
                  >
                    {genderData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                </PieChart>
              </div>
            </div>

            {/* Edad */}
            <div className="statistics-card">
              <h3>Distribución por Edad</h3>
              <BarChart width={300} height={300} data={ageData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#FF914D">
                  {ageData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[0]} />
                  ))}
                </Bar>
              </BarChart>
            </div>

            {/* Mapa */}
            <div className="statistics-card">
              <h3>Distribución Geográfica</h3>
              <div className="chart-container" style={{ height: "250px" }}>
                <AndalusiaMap />
              </div>
            </div>

            {/* Notas */}
            <div className="notebook-card">
              <h3>Pacientes y sus estadísticas</h3>
              <div className="notebook-content">
                <p>
                  <strong>Total de pacientes:</strong> 1,248 registrados en el sistema
                </p>
                <p>
                  <strong>Consultas mensuales:</strong> 342 consultas en el último mes
                </p>
                <p>
                  <strong>Patologías más comunes:</strong> Hipertensión (24%), Diabetes (18%), Problemas respiratorios
                  (15%)
                </p>
                <p>
                  <strong>Tiempo medio de consulta:</strong> 12 minutos por paciente
                </p>
                <p>
                  <strong>Satisfacción del paciente:</strong> 4.7/5 basado en 856 valoraciones
                </p>
                <p>
                  <strong>Tendencia de uso:</strong> Incremento del 12% respecto al mes anterior
                </p>
                <p>
                  <strong>Pacientes recurrentes:</strong> 68% han realizado más de una consulta
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default StatisticsDialog

