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
        estasLogueado(){
            if(this.authId == null){
                window.location="/login";
            }
            this.authId = localStorage.getItem("libros_flaites_id");
            this.authNombre = localStorage.getItem("libros_flaites_nombre");
            this.authToken = localStorage.getItem("libros_flaites_token");
        },
        cerrarSesion(){
            
            if(window.confirm("Cerrar sesion...")){
                localStorage.clear();
                window.location = "/login";
            }
        },
    },
});

