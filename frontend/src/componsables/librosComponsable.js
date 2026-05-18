import { readonly, ref } from "vue";
const API_URL = import.meta.env.VITE_API_URL;

export function librosComposable(){

    // Variables:
    const datos = ref({
        data: [],
        pagina_actual: 1,
        total_paginas: 1,
        total_registros: 0,
        hay_siguiente: false,
        hay_anterior: false
    });
    const error = ref(null);

    // Obtener datos:
    const getDatos = async(page = 1) => {

        try {
            const res = await fetch(`${API_URL}libros?page=${page}`, {
                headers: {
                    'content-type': 'application/json'
                }
            });

            if(!res.ok){
                throw new Error('Error al obtener datos');
            }

            datos.value = await res.json();
        } catch (e) {
            error.value = e;
        }
    };

    // Carga inicial:
    getDatos();

    return{
        datos: readonly(datos),
        error: readonly(error),
        getDatos
    }
}


