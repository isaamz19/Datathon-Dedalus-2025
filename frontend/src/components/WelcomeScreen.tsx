import "../styles/WelcomeScreen.css"

type WelcomeScreenProps = {
  onStart: () => void
}

const WelcomeScreen = ({ onStart }: WelcomeScreenProps) => {
  return (
    <div className="welcome-container">
      <div className="welcome-content">
        {/* Espacio para la imagen del robot */}
        <div className="robot-image-placeholder">{/* El usuario colocará su imagen aquí */}</div>

        <h1 className="welcome-title">DR. DIAGNOBOT</h1>

        <button className="start-button" onClick={onStart}>
          EMPEZAR
        </button>
      </div>
    </div>
  )
}

export default WelcomeScreen

