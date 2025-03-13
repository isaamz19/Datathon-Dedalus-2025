import "../styles/ConsultasSidebar.css"
import React, { useState } from 'react';

const ConsultasSidebar = () => {

  // Estado para controlar la visibilidad de la barra lateral
  const [isSidebarVisible, setSidebarVisible] = useState(false);

  // Funcion para alternar la visibilidad de la barra lateral
  const toggleSidebar = () => {
      setSidebarVisible(!isSidebarVisible);
  };

  const consultas = ["CONSULTA 1", "CONSULTA 2", "CONSULTA 3", "CONSULTA 4", "CONSULTA 5", "CONSULTA 6"]

  return (
    <div className="consultas-container">
      {/*Boton para mostrar la barra lateral */}
      <button id="menuToggle" onClick={toggleSidebar}>☰</button>
          {/*Barra lateral*/}
          <div id="sidebar" className={isSidebarVisible ? 'active' : ''}>
              {/*Boton para ocultar la barra lateral */}
              <button id="closeMenu" onClick={toggleSidebar}>☰</button>
          </div>
      {consultas.map((consulta, index) => (
        <button key={index} className="consulta-button">
          {consulta}
        </button>
      ))}
    </div>
  )
}

export default ConsultasSidebar

