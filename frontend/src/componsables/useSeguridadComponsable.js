import { useAuthStore } from "@/stores/authStore";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;

export function loginComposable(body){

    const sendData = async(body) => {

        axios.post(`${API_URL}seguridad/login`, body, {
            headers: {
                'content-type': "application/json"
            }
        }).then((response) => {
            const store = useAuthStore();
            store.iniciarSesion(response.data);
            window.location="/panel";
        })
        .catch((err) =>  {
            alert("Error al iniciar sesion");
            window.location = location.href;
        })
        
    };

    return {
        sendData
    };

}

/*
try {
            axios.post(`${API_URL}seguridad/login`);
        } catch (error) {
            alert("Error inesperado");
            window.location = location.href;
        }
*/

