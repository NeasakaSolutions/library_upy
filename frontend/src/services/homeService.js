const API_URL = import.meta.env.VITE_API_URL;

export async function getDatosHome(){

    // Realizar peticion al endpoint:
    const respuesta = await fetch(`${API_URL}libros-home`, {
        headers: {
        'content-type': 'application/json'
        }
    });

    // Validar si ocurrio un error HTTP:
    if (!respuesta.ok) {
        throw new Error('Error al obtener los datos');
    }

    return await respuesta.json();
}