<script setup>
import { librosComposable } from '@/componsables/librosComponsable';
import { watchEffect, ref } from 'vue';
import { Form, Field } from 'vee-validate';


const { datos: libros, error, categorias, getDatos} = librosComposable();

// Manejo de errores:
watchEffect(() => {

    if(error.value){
        //console.log("Error con la api: " + error.value)
        window.location = '/error'
    }
});

const categoria_id = ref("0");
const search = ref("");

let enviar = () => {

    window.location =
    `/libros/buscador?categoria_id=${categoria_id.value}&search=${search.value}`;

};

</script>

<template>
<header>

    <nav class="navbar navbar-expand-lg navbar-dark cyber-navbar">

        <div class="container-fluid">

            <!-- LOGO -->
            <router-link class="navbar-brand d-flex align-items-center gap-2" to="/">
                <img src="/img/core-img/favicon.ico" width="40" alt="logo">
            </router-link>

            <!-- TOGGLER -->
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#menu">
                <span class="navbar-toggler-icon"></span>
            </button>

            <!-- MENU -->
            <div class="collapse navbar-collapse justify-content-end" id="menu">


                <!-- LINKS -->
                <ul class="navbar-nav align-items-lg-center gap-lg-3">

                    <li class="nav-item">
                        <router-link class="nav-link" to="/">Inicio</router-link>
                    </li>

                    <li class="nav-item">
                        <router-link class="nav-link" to="/libros">Libros</router-link>
                    </li>

                    <li class="nav-item">
                        <router-link class="nav-link" to="/login">
                            Iniciar sesión
                        </router-link>
                    </li>

                </ul>

                <!-- BUSCADOR -->
                <Form
                    @submit="enviar"
                    class="search-box"
                >

                    <!-- SELECT -->
                    <Field
                        as="select"
                        v-model="categoria_id"
                        class="search-input"
                        name="categoria">

                        <option disabled selected value="0">
                            Buscar categoría...
                        </option>

                        <option
                            v-for="(categoria, i) in categorias?.data"
                            :key="i"
                            :value="categoria.id">

                            {{ categoria.nombre }}
                        </option>

                    </Field>

                    <!-- INPUT -->
                    <Field
                        class="search-input"
                        v-model="search"
                        type="search"
                        name="buscar"
                        placeholder="Buscar libro..."/>

                    <!-- BOTON -->
                    <button
                        class="search-btn"
                        type="submit">

                        <i class="fa fa-search"></i>

                    </button>

                </Form>
                

            </div>

        </div>

    </nav>

</header>
</template>

<style scoped>
/* OPTION DEFAULT */
select.search-input option {

    background: #121a2a;

    color: white;
}

/* TEXTO DEL SELECT */
select.search-input {

    color: rgba(255,255,255,0.45);

    background: rgba(255,255,255,0.06);
}

select.search-input:invalid {

    color: rgba(255,255,255,0.55);
}
</style>