import { defineStore } from "pinia";


export const useAuthStore = defineStore('auth', {

    state:() => ({
        authId: (localStorage.getItem('libros_flaites_id') != null) ? localStorage.getItem('libros_flaites_id'): null,
        authNombre: (localStorage.getItem('libros_flaites_nombre') != null) ? localStorage.getItem('libros_flaites_nombre'): null,
        authToken: (localStorage.getItem('libros_flaites_token') != null) ? localStorage.getItem('libros_flaites_token'): null
    }),
    actions: {
        iniciarSesion(data){
            localStorage.setItem('libros_flaites_id', data.id);
            localStorage.setItem('libros_flaites_nombre', data.nombre);
            localStorage.setItem('libros_flaites_token', data.token);
        },
    },
});

