import { useAuthStore } from "@/stores/authStore";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

// ========================================
// REGISTRO DE USUARIOS
// ========================================
export function registroComposable() {
    const sendData = async (body) => {
        try {
            const response = await axios.post(
                `${API_URL}seguridad/registro`,
                body,
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            alert(
                response.data.mensaje ||
                "Te has registrado correctamente. En unos momentos un administrador revisará tu solicitud."
            );

            return true;

        } catch (error) {
            console.error("Error al registrar usuario:", error);

            const mensaje =
                error.response?.data?.mensaje ||
                error.response?.data?.error ||
                "Ocurrió un error al registrar tus datos. Inténtalo nuevamente.";

            alert(mensaje);

            return false;
        }
    };

    return { sendData };
}

// ========================================
// INICIO DE SESIÓN
// ========================================
export function loginComposable() {
    const sendData = async (body) => {
        try {
            const response = await axios.post(
                `${API_URL}seguridad/login`,
                body,
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            const store = useAuthStore();

            store.iniciarSesion(response.data);

            window.location.href = "/panel";

            return true;

        } catch (error) {
            console.error("Error al iniciar sesión:", error);

            const mensaje =
                error.response?.data?.mensaje ||
                error.response?.data?.error ||
                "Error al iniciar sesión. Verifica tus credenciales.";

            alert(mensaje);

            return false;
        }
    };

    return { sendData };
}

/*
try {
            axios.post(`${API_URL}seguridad/login`);
        } catch (error) {
            alert("Error inesperado");
            window.location = location.href;
        }
*/

