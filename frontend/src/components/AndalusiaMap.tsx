"use client"

import { useState } from "react"
import "../styles/AndalusiaMap.css"

// Datos de ejemplo para las provincias de Andalucía
const provincesData = [
  { id: "almeria", name: "ALMERÍA", value: 12 },
  { id: "cadiz", name: "CÁDIZ", value: 18 },
  { id: "cordoba", name: "CÓRDOBA", value: 15 },
  { id: "granada", name: "GRANADA", value: 22 },
  { id: "huelva", name: "HUELVA", value: 8 },
  { id: "jaen", name: "JAÉN", value: 10 },
  { id: "malaga", name: "MÁLAGA", value: 30 },
  { id: "sevilla", name: "SEVILLA", value: 25 },
]

// Función para obtener el color basado en el valor
const getColor = (value: number) => {
  const opacity = Math.max(0.1, Math.min(1, value / 30))
  return `rgba(255, 145, 77, ${opacity})`
}

const AndalusiaMap = () => {
  const [hoveredProvince, setHoveredProvince] = useState<string | null>(null)

  return (
    <div className="map-container">
      <svg className="andalusia-map" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
        {/* Huelva */}
        <g onMouseEnter={() => setHoveredProvince("huelva")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M50,100 L100,80 L120,140 L70,160 Z"
            fill={getColor(provincesData.find((p) => p.id === "huelva")?.value || 0)}
          />
          <text x="85" y="120" className="province-name">
            HUELVA
            {hoveredProvince === "huelva" && (
              <tspan x="85" y="135" className="province-value">
                {provincesData.find((p) => p.id === "huelva")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Sevilla */}
        <g onMouseEnter={() => setHoveredProvince("sevilla")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M100,80 L160,70 L180,130 L120,140 Z"
            fill={getColor(provincesData.find((p) => p.id === "sevilla")?.value || 0)}
          />
          <text x="140" y="105" className="province-name">
            SEVILLA
            {hoveredProvince === "sevilla" && (
              <tspan x="140" y="120" className="province-value">
                {provincesData.find((p) => p.id === "sevilla")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Córdoba */}
        <g onMouseEnter={() => setHoveredProvince("cordoba")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M160,70 L220,60 L240,120 L180,130 Z"
            fill={getColor(provincesData.find((p) => p.id === "cordoba")?.value || 0)}
          />
          <text x="200" y="95" className="province-name">
            CÓRDOBA
            {hoveredProvince === "cordoba" && (
              <tspan x="200" y="110" className="province-value">
                {provincesData.find((p) => p.id === "cordoba")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Jaén */}
        <g onMouseEnter={() => setHoveredProvince("jaen")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M220,60 L280,50 L300,110 L240,120 Z"
            fill={getColor(provincesData.find((p) => p.id === "jaen")?.value || 0)}
          />
          <text x="260" y="85" className="province-name">
            JAÉN
            {hoveredProvince === "jaen" && (
              <tspan x="260" y="100" className="province-value">
                {provincesData.find((p) => p.id === "jaen")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Cádiz */}
        <g onMouseEnter={() => setHoveredProvince("cadiz")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M70,160 L120,140 L140,180 L90,200 Z"
            fill={getColor(provincesData.find((p) => p.id === "cadiz")?.value || 0)}
          />
          <text x="105" y="170" className="province-name">
            CÁDIZ
            {hoveredProvince === "cadiz" && (
              <tspan x="105" y="185" className="province-value">
                {provincesData.find((p) => p.id === "cadiz")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Málaga */}
        <g onMouseEnter={() => setHoveredProvince("malaga")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M140,180 L180,130 L240,120 L220,170 Z"
            fill={getColor(provincesData.find((p) => p.id === "malaga")?.value || 0)}
          />
          <text x="190" y="150" className="province-name">
            MÁLAGA
            {hoveredProvince === "malaga" && (
              <tspan x="190" y="165" className="province-value">
                {provincesData.find((p) => p.id === "malaga")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Granada */}
        <g onMouseEnter={() => setHoveredProvince("granada")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M240,120 L300,110 L280,170 L220,170 Z"
            fill={getColor(provincesData.find((p) => p.id === "granada")?.value || 0)}
          />
          <text x="260" y="140" className="province-name">
            GRANADA
            {hoveredProvince === "granada" && (
              <tspan x="260" y="155" className="province-value">
                {provincesData.find((p) => p.id === "granada")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Almería */}
        <g onMouseEnter={() => setHoveredProvince("almeria")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M220,170 L280,170 L300,210 L240,200 Z"
            fill={getColor(provincesData.find((p) => p.id === "almeria")?.value || 0)}
          />
          <text x="260" y="190" className="province-name">
            ALMERÍA
            {hoveredProvince === "almeria" && (
              <tspan x="260" y="205" className="province-value">
                {provincesData.find((p) => p.id === "almeria")?.value}%
              </tspan>
            )}
          </text>
        </g>
      </svg>
    </div>
  )
}

export default AndalusiaMap

