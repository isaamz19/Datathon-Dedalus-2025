import type React from "react"
import { useState, useEffect, useRef } from "react"
import { Mic, ArrowUpCircle } from "lucide-react"
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
  const textAreaRef = useRef<HTMLTextAreaElement | null>(null)

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

        setMessage(finalTranscript || interimTranscript); // Cambio: solo actualiza el mensaje con el texto final o interino

      };

      setRecognition(newRecognition);
    } else {
      console.warn("Tu navegador no soporta la API de reconocimiento de voz.");
    }
  }, [])

  // Ajustar el tamaño del textarea
  useEffect(() => {
    if (textAreaRef.current) {
      textAreaRef.current.style.height = "auto"; // Resetear la altura
      textAreaRef.current.style.height = `${textAreaRef.current.scrollHeight}px`; // Ajustar la altura
    }
  }, [message]) // Cada vez que el mensaje cambia, ajustar el tamaño

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

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSubmit(e as unknown as React.FormEvent)  // Enviar el mensaje al presionar ENTER
    }
  }

  return (
    <form className="chat-input-container" onSubmit={handleSubmit}>
      <textarea
        // type="text"
        ref={textAreaRef} // Asignar la referencia aquí
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown} // Detectar el ENTER
        placeholder="ESCRIBE A DR. DIAGNOBOT"
        disabled={isLoading}
        className="chat-input"
      />
      <button
        type="submit"
        className="send-button"
        aria-label="Enviar mensaje"
        disabled={isLoading}
      >
        <ArrowUpCircle size={24} /> {/* Flecha de enviar */}
      </button>
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

