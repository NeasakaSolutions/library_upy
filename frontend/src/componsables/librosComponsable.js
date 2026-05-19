import { readonly, ref } from "vue";
import { useRoute } from "vue-router";
const API_URL = import.meta.env.VITE_API_URL;

export function librosComposable(){

    const route = useRoute();

    // Variables:
    const datos = ref({
        data: [],
        pagina_actual: 1,
        total_paginas: 1,
        total_registros: 0,
        hay_siguiente: false,
        hay_anterior: false
    });
    const categorias = ref({
        data: []
    });
    const error = ref(null);

    // Obtener datos:
    const getDatos = async(page = 1) => {

        
        let url;
        
        if(route.query.categoria_id){
            url = `${API_URL}libros-buscador?categoria_id=${route.query.categoria_id}&search=${route.query.search}`
        } else {
            url = `${API_URL}libros?page=${page}`
        }

        try {
            const res = await fetch(url, {
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
    /*
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
    */

    // Carga inicial:
    getDatos();

    // Obtener datos:
    const getCategorias = async() => {

        try {
            const res = await fetch(`${API_URL}categorias`, {
                headers: {
                    'content-type': 'application/json'
                }
            });

            if(!res.ok){
                throw new Error('Error al obtener datos');
            }

            categorias.value = await res.json();
        } catch (e) {
            error.value = e;
        }
    };

    getCategorias();

    return{
        datos: readonly(datos),
        error: readonly(error),
        categorias: readonly(categorias),
        getDatos
    }
}


