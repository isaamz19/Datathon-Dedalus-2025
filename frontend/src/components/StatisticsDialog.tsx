"use client"

import { useEffect, useState } from "react"
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"
import { X, Loader } from "lucide-react"
import "../styles/StatisticsDialog.css"

// Definición de tipos para los datos de estadísticas
type GenderData = { name: string; value: number }[]
type AgeData = { name: string; value: number }[]
type PathologyData = { name: string; value: number }[]
type ProvinciasData = { name: string; value: number }[]

// Tipo para los datos de resumen
type SummaryData = {
  totalPatients: number
}

// Tipo para todos los datos de estadísticas (coincide con la estructura de la API)
type StatisticsData = {
  summaryData: SummaryData
  genderData: GenderData
  ageData: AgeData
  provinciasData: ProvinciasData
  pathologyData: PathologyData
}

const COLORS = ["#FF914D", "#B8D2AD", "#EAE2DA", "#9FAD86", "#CFBDAA"]

// URL base del backend
const API_BASE_URL = "http://localhost:5000"

type StatisticsDialogProps = {
  isOpen: boolean
  onClose: () => void
}

const StatisticsDialog = ({ isOpen, onClose }: StatisticsDialogProps) => {
  // Estados para los datos de estadísticas
  const [statisticsData, setStatisticsData] = useState<StatisticsData | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Función para cargar los datos de estadísticas
  const fetchStatistics = async () => {
    if (!isOpen) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE_URL}/api/get-estadistic`)

      if (!response.ok) {
        throw new Error(`Error al obtener estadísticas: ${response.status}`)
      }

      const data = await response.json()
      setStatisticsData(data)
    } catch (err) {
      console.error("Error al cargar estadísticas:", err)
      setError("No se pudieron cargar las estadísticas. Por favor, inténtalo de nuevo más tarde.")
    } finally {
      setIsLoading(false)
    }
  }

  // Cargar datos cuando se abre el diálogo
  useEffect(() => {
    if (isOpen) {
      fetchStatistics()
    }
  }, [isOpen])

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
          {isLoading ? (
            <div className="loading-container">
              <Loader className="spinner" size={40} />
              <p>Cargando estadísticas...</p>
            </div>
          ) : error ? (
            <div className="error-container">
              <p>{error}</p>
              <button className="retry-button" onClick={fetchStatistics}>
                Reintentar
              </button>
            </div>
          ) : statisticsData ? (
            <>
              {/* Resumen de Pacientes - Parte superior */}
              <div className="patient-summary-card">
                <h3>Resumen de Pacientes</h3>
                <div className="total-patients-container">
                  <div className="total-patients-value">
                    {statisticsData.summaryData.totalPatients.toLocaleString()}
                  </div>
                  <div className="total-patients-label">Total de pacientes</div>
                </div>

                {/* Patologías más comunes como gráfico */}
                <h4 className="pathology-title">Patologías más comunes</h4>
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie
                      data={statisticsData.pathologyData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    >
                      {statisticsData.pathologyData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              {/* Gráficos inferiores */}
              <div className="statistics-grid">
                {/* Género */}
                <div className="statistics-card">
                  <h3>Distribución por Género</h3>
                  <div className="chart-container">
                    <PieChart width={300} height={300}>
                      <Pie
                        data={statisticsData.genderData}
                        cx={150}
                        cy={150}
                        innerRadius={60}
                        outerRadius={100}
                        fill="#8884d8"
                        paddingAngle={5}
                        dataKey="value"
                        label={({ name, value }) => `${name}: ${value}%`}
                      >
                        {statisticsData.genderData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                    </PieChart>
                  </div>
                </div>

                {/* Edad */}
                <div className="statistics-card">
                  <h3>Distribución por Edad</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={statisticsData.ageData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="#FF914D">
                        {statisticsData.ageData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[0]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* Provincias */}
                <div className="statistics-card">
                  <h3>Distribución por Provincia</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart
                      data={statisticsData.provinciasData}
                      layout="vertical"
                      margin={{ top: 5, right: 30, left: 50, bottom: 5 }}
                    >
                      <XAxis type="number" />
                      <YAxis type="category" dataKey="name" />
                      <Tooltip />
                      <Bar dataKey="value" fill="#FF914D" label={{ position: "right", fill: "#666" }}>
                        {statisticsData.provinciasData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[0]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </>
          ) : (
            <div className="error-container">
              <p>No hay datos disponibles</p>
              <button className="retry-button" onClick={fetchStatistics}>
                Reintentar
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export default StatisticsDialog

