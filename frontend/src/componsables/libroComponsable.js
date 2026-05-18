import { readonly, ref } from "vue";
const API_URL = import.meta.env.VITE_API_URL;

export function libroComposable(id, slug){

    // Variables:
    const datos = ref({});
    const error = ref(null);

    // Obtener datos:
    const getDatos = async() => {

        try {
            const res = await fetch(`${API_URL}libros/slug/${id}/${slug}`, {
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
    getDatos(id, slug);

    return{
        datos: readonly(datos),
        error: readonly(error),
        getDatos
    }
}


