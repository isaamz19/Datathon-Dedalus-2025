"use client"

import { useState } from "react"
import "../styles/AndalusiaMap.css"

// Datos de ejemplo para las provincias de Andalucía
const provincesData = [
  { id: "almeria", name: "ALMERÍA", value: 12, center: [320, 180] },
  { id: "cadiz", name: "CÁDIZ", value: 18, center: [80, 180] },
  { id: "cordoba", name: "CÓRDOBA", value: 15, center: [160, 100] },
  { id: "granada", name: "GRANADA", value: 22, center: [280, 140] },
  { id: "huelva", name: "HUELVA", value: 8, center: [60, 120] },
  { id: "jaen", name: "JAÉN", value: 10, center: [220, 80] },
  { id: "malaga", name: "MÁLAGA", value: 30, center: [200, 160] },
  { id: "sevilla", name: "SEVILLA", value: 25, center: [120, 140] },
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
            d="M40,100 L80,80 L100,140 L60,160 Z"
            fill={getColor(provincesData.find((p) => p.id === "huelva")?.value || 0)}
          />
          <text x="60" y="120" className="province-name">
            HUELVA
            {hoveredProvince === "huelva" && (
              <tspan x="60" y="135" className="province-value">
                {provincesData.find((p) => p.id === "huelva")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Sevilla */}
        <g onMouseEnter={() => setHoveredProvince("sevilla")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M80,80 L140,70 L160,130 L100,140 Z"
            fill={getColor(provincesData.find((p) => p.id === "sevilla")?.value || 0)}
          />
          <text x="120" y="110" className="province-name">
            SEVILLA
            {hoveredProvince === "sevilla" && (
              <tspan x="120" y="125" className="province-value">
                {provincesData.find((p) => p.id === "sevilla")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Córdoba */}
        <g onMouseEnter={() => setHoveredProvince("cordoba")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M140,70 L200,60 L220,120 L160,130 Z"
            fill={getColor(provincesData.find((p) => p.id === "cordoba")?.value || 0)}
          />
          <text x="160" y="100" className="province-name">
            CÓRDOBA
            {hoveredProvince === "cordoba" && (
              <tspan x="160" y="115" className="province-value">
                {provincesData.find((p) => p.id === "cordoba")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Jaén */}
        <g onMouseEnter={() => setHoveredProvince("jaen")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M200,60 L260,50 L280,110 L220,120 Z"
            fill={getColor(provincesData.find((p) => p.id === "jaen")?.value || 0)}
          />
          <text x="220" y="80" className="province-name">
            JAÉN
            {hoveredProvince === "jaen" && (
              <tspan x="220" y="95" className="province-value">
                {provincesData.find((p) => p.id === "jaen")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Cádiz */}
        <g onMouseEnter={() => setHoveredProvince("cadiz")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M60,160 L100,140 L120,180 L80,200 Z"
            fill={getColor(provincesData.find((p) => p.id === "cadiz")?.value || 0)}
          />
          <text x="80" y="170" className="province-name">
            CÁDIZ
            {hoveredProvince === "cadiz" && (
              <tspan x="80" y="185" className="province-value">
                {provincesData.find((p) => p.id === "cadiz")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Málaga */}
        <g onMouseEnter={() => setHoveredProvince("malaga")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M120,180 L160,130 L220,120 L240,160 L180,190 Z"
            fill={getColor(provincesData.find((p) => p.id === "malaga")?.value || 0)}
          />
          <text x="180" y="160" className="province-name">
            MÁLAGA
            {hoveredProvince === "malaga" && (
              <tspan x="180" y="175" className="province-value">
                {provincesData.find((p) => p.id === "malaga")?.value}%
              </tspan>
            )}
          </text>
        </g>

        {/* Granada */}
        <g onMouseEnter={() => setHoveredProvince("granada")} onMouseLeave={() => setHoveredProvince(null)}>
          <path
            className="province"
            d="M220,120 L280,110 L300,150 L240,160 Z"
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
            d="M240,160 L300,150 L320,190 L260,200 Z"
            fill={getColor(provincesData.find((p) => p.id === "almeria")?.value || 0)}
          />
          <text x="280" y="180" className="province-name">
            ALMERÍA
            {hoveredProvince === "almeria" && (
              <tspan x="280" y="195" className="province-value">
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

