import type React from "react"
import { useState, useEffect } from "react"
import { Mic } from "lucide-react"
import "../styles/ChatInput.css"

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message?: string;
}

interface SpeechRecognitionResult {
  isFinal: boolean;
  [index: number]: {
    transcript: string;
    confidence: number;
  };
}

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
}

interface SpeechRecognitionResultList {
  length: number;
  [index: number]: SpeechRecognitionResult;
}

interface SpeechRecognition extends EventTarget {
  start(): void;
  stop(): void;
  onstart?: () => void;
  onend?: () => void;
  onerror?: (event: SpeechRecognitionErrorEvent) => void;
  onresult?: (event: SpeechRecognitionEvent) => void;
  lang?: string;
  continuous?: boolean;
  interimResults?: boolean;
}

type ChatInputProps = {
  onSendMessage: (message: string) => void
  isLoading: boolean
}

const ChatInput = ({ onSendMessage, isLoading }: ChatInputProps) => {
  const [message, setMessage] = useState("")
  const [isListening, setIsListening] = useState(false)
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(null)

  useEffect(() => {
    if ("SpeechRecognition" in window || "webkitSpeechRecognition" in window) {
      const SpeechRecognitionAPI =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const newRecognition = new SpeechRecognitionAPI();

      newRecognition.lang = "es-ES";
      newRecognition.continuous = false;
      newRecognition.interimResults = true;  // Activa texto en tiempo real

      newRecognition.onstart = () => setIsListening(true);
      newRecognition.onend = () => setIsListening(false);
      newRecognition.onerror = (event: SpeechRecognitionErrorEvent) => {
        console.error("Error en reconocimiento de voz:", event.error);
        setIsListening(false);
      };

      newRecognition.onresult = (event: SpeechRecognitionEvent) => {
        let interimTranscript = "";
        let finalTranscript = "";

        const resultsArray = Array.from(event.results); // Convierte a array
        for (const result of resultsArray) {
          const transcript = result[0].transcript;
          if (result.isFinal) {
            finalTranscript += transcript + " ";
          } else {
            interimTranscript += transcript + " ";
          }
        }

        setMessage((prev) => prev + (finalTranscript || interimTranscript)); // Aquí solo actualizamos el texto en tiempo real sin enviarlo automáticamente

      };

      setRecognition(newRecognition);
    } else {
      console.warn("Tu navegador no soporta la API de reconocimiento de voz.");
    }
  }, [onSendMessage])

  // Función de manejo de submit (solo se llama cuando el usuario hace clic en enviar)
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message); // Envía el mensaje solo cuando el usuario hace clic
      setMessage(""); // Limpiar el campo de entrada
    }
  }

  const handleMicClick = () => {
    if (recognition) {
      if (isListening) {
        recognition.stop();
      } else {
        recognition.start();
      }
    }
  };

  return (
    <form className="chat-input-container" onSubmit={handleSubmit}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="ESCRIBE A DR. DIAGNOBOT"
        disabled={isLoading}
        className="chat-input"
      />
      <button
        type="button"
        className={`mic-button ${isListening ? "listening" : ""}`}
        aria-label="Usar micrófono"
        onClick={handleMicClick}
      >
        <Mic />
      </button>
    </form>
  )
}

export default ChatInput

