import { useEffect, useState, useRef, useCallback } from "react"
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"
import { X, Loader, Download, Info } from "lucide-react"
import "../styles/StatisticsDialog.css"
import html2canvas from "html2canvas"
import jsPDF from "jspdf"

// Definición de tipos para los datos de estadísticas
type GenderData = { name: string; value: number }[]
type AgeData = { name: string; value: number }[]
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
}

// URL base del backend
const API_BASE_URL = "http://localhost:5000"

type StatisticsDialogProps = {
  isOpen: boolean
  onClose: () => void
}

const StatisticsDialog = ({ isOpen, onClose }: StatisticsDialogProps) => {
  const [statisticsData, setStatisticsData] = useState<StatisticsData | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showInfo, setShowInfo] = useState(false)
  const contentRef = useRef<HTMLDivElement>(null)

  // Función para obtener colores adaptados al tema actual
  const getThemeColors = useCallback(() => {
    const theme = document.documentElement.getAttribute("data-theme") || "light"

    switch (theme) {
      case "dark":
        return ["#FFA76B", "#D8F0CC", "#BFCCa8", "#E0D0C0", "#F5F0EB"]
      case "colorblind":
        return ["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51"]
      case "dyslexia":
        return ["#1D3557", "#457B9D", "#A8DADC", "#F1FAEE", "#E63946"]
      default:
        return ["#FF914D", "#B8D2AD", "#9FAD86", "#CFBDAA", "#EAE2DA"]
    }
  }, [])

  const [COLORS, setColors] = useState(getThemeColors())

  // Actualizar colores cuando cambia el tema
  useEffect(() => {
    setColors(getThemeColors())

    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === "attributes" && mutation.attributeName === "data-theme") {
          setColors(getThemeColors())
        }
      })
    })

    observer.observe(document.documentElement, { attributes: true })

    return () => observer.disconnect()
  }, [getThemeColors])

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
      setStatisticsData(data as StatisticsData)
    } catch (err) {
      console.error("Error al cargar estadísticas:", err)
      setError("No se pudieron cargar las estadísticas. Por favor, inténtalo de nuevo más tarde.")
    } finally {
      setIsLoading(false)
    }
  }

  const downloadAsPDF = async () => {
    if (!contentRef.current) return

    try {
      const loadingElement = document.createElement("div")
      loadingElement.className = "pdf-loading"
      loadingElement.textContent = "Generando PDF..."
      document.body.appendChild(loadingElement)

      const canvas = await html2canvas(contentRef.current, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: getComputedStyle(document.documentElement).getPropertyValue("--background-color"),
      })

      const imgData = canvas.toDataURL("image/png")
      const pdf = new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "a4",
      })

      const imgWidth = 210
      const imgHeight = (canvas.height * imgWidth) / canvas.width

      pdf.addImage(imgData, "PNG", 0, 0, imgWidth, imgHeight)
      pdf.save("estadisticas-dr-diagnobot.pdf")

      document.body.removeChild(loadingElement)
    } catch (err) {
      console.error("Error al generar PDF:", err)
      alert("Hubo un error al generar el PDF. Por favor, inténtalo de nuevo.")
    }
  }

  useEffect(() => {
    if (isOpen) {
      fetchStatistics()
    }
  }, [isOpen])

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
          <div className="header-buttons">
            <button
              className="info-button"
              onClick={() => setShowInfo(!showInfo)}
              aria-label="Información"
              title="Mostrar información"
            >
              <Info size={20} />
            </button>
            <button
              className="download-button"
              onClick={downloadAsPDF}
              aria-label="Descargar PDF"
              title="Descargar como PDF"
            >
              <Download size={20} />
            </button>
            <button className="close-button" onClick={onClose} aria-label="Cerrar" title="Cerrar">
              <X size={24} />
            </button>
          </div>
        </div>

        {showInfo && (
          <div className="info-panel">
            <h3>Acerca de estas estadísticas</h3>
            <p>
              Estos datos representan información demográfica y médica anonimizada de los pacientes. Las estadísticas se
              actualizan periódicamente y pueden descargarse en formato PDF para su análisis posterior.
            </p>
            <p>
              <strong>Nota:</strong> Todos los datos mostrados cumplen con la normativa de protección de datos y han
              sido procesados para garantizar el anonimato de los pacientes.
            </p>
            <button className="close-info-button" onClick={() => setShowInfo(false)}>
              Cerrar información
            </button>
          </div>
        )}

        <div className="statistics-content" ref={contentRef}>
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
              <div className="patient-summary-card">
                <h3>Resumen de Pacientes</h3>
                <div className="summary-content">
                  <div className="total-patients-container">
                    <div className="total-patients-value">
                      {statisticsData.summaryData.totalPatients.toLocaleString()}
                    </div>
                    <div className="total-patients-label">Total de pacientes</div>
                  </div>

                  <div className="summary-description">
                    <h4>Análisis de datos</h4>
                    <p>
                      Los datos presentados muestran la distribución demográfica de los pacientes según género, edad y
                      ubicación geográfica. Esta información es valiosa para entender mejor la composición de nuestra
                      población de pacientes y adaptar nuestros servicios a sus necesidades específicas.
                    </p>
                  </div>
                </div>
              </div>

              <div className="statistics-grid">
                <div className="statistics-card">
                  <h3>Distribución por Género</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={statisticsData.genderData}
                        cx="50%"
                        cy="50%"
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
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>

                <div className="statistics-card">
                  <h3>Distribución por Edad</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={statisticsData.ageData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="#FF914D">
                        {statisticsData.ageData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div className="statistics-card full-width">
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
                      <Bar dataKey="value" fill="#FF914D">
                        {statisticsData.provinciasData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
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

