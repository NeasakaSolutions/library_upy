<script setup>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import { librosComposable } from '@/componsables/librosComponsable';
import { watchEffect } from 'vue';
// npm i vee-validate --save
// npm i @vee-validate/yup

const { datos: libros, error, getDatos} = librosComposable();

// Manejo de errores:
watchEffect(() => {

    if(error.value){
        //console.log("Error con la api: " + error.value)
        window.location = '/error'
    }
});

const cambiarPagina = async(pagina) => {

    if(pagina < 1 || pagina > libros.value.total_paginas){
        return;
    }

    await getDatos(pagina);

}

</script>

<template>

<Header></Header>

<!-- =====================================================================================
     HERO
===================================================================================== -->
<div
    class="breadcumb-area bg-img bg-overlay cyber-hero"
    style="background-image: url('/img/bg-img/portada_home.jpeg')"
>

    <div class="container h-100">

        <div class="row h-100 align-items-center">

            <div class="col-12">

            </div>

        </div>

    </div>

</div>

<!-- =====================================================================================
     RECURSOS
===================================================================================== -->
<section class="cyber-section pt-0">

    <div class="container">

        <!-- TITULO -->
        <div class="row">

            <div class="col-12">

                <div class="text-center mb-5">

                    <h3 class="text-light">
                        Todos nuestros libros
                    </h3>

                </div>

            </div>

        </div>

        <!--CARDS-->
        <div class="row g-4 mobile-spacing">

                <div v-for = "(libro, index) in libros.data" :key = "index" class="col-12 col-md-6 col-lg-4">
                    <router-link :to = "{name: 'librosDetalle', params:{id:libro.id, slug: libro.slug}}">
                        <div class="cyber-book h-100">
                            <img :src="libro.imagen" class="foto-mini w-100" :alt="libro.nombre">
                            <div class="receipe-content p-3">
                                <h5 class="text-light">{{ libro.nombre }}</h5>
                                <p>Autor: {{ libro.autor }}</p>
                            </div>
                        </div>
                    </router-link>
                </div>

        </div>

        <!-- PAGINACION -->
<div class="row mt-5">

    <div class="col-12">

        <div class="d-flex justify-content-center align-items-center gap-2 flex-wrap">

            <!-- ANTERIOR -->
            <button
                class="btn cyber-page-btn"
                :disabled="!libros.hay_anterior"
                @click="cambiarPagina(libros.pagina_actual - 1)"
            >
                Anterior
            </button>

            <!-- NUMEROS -->
            <button
                v-for="pagina in libros.total_paginas"
                :key="pagina"
                class="btn cyber-page-btn"
                :class="{
                    active: pagina === libros.pagina_actual
                }"
                @click="cambiarPagina(pagina)"
            >
                {{ pagina }}
            </button>

            <!-- SIGUIENTE -->
            <button
                class="btn cyber-page-btn"
                :disabled="!libros.hay_siguiente"
                @click="cambiarPagina(libros.pagina_actual + 1)"
            >
                Siguiente
            </button>

        </div>

    </div>

</div>

    </div>

</section>

<Footer></Footer>

</template>

<style scoped>

:global(body) {
    background: #0b0f1a;
    margin: 0;
}

/* =====================================================================================
   TITULOS HERO
===================================================================================== */
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;

    margin-bottom: 15px;
}

.hero-subtitle {
    color: rgba(255,255,255,0.75);

    max-width: 700px;

    margin: auto;

    line-height: 1.7;
}

/* =====================================================================================
   BUSCADOR
===================================================================================== */
.search-container {
    background: #121a2a;

    border: 1px solid rgba(176, 38, 255, 0.12);

    border-radius: 18px;

    padding: 30px;
}

/* INPUTS */
.cyber-input {
    background: rgba(255,255,255,0.05) !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    color: white !important;

    height: 50px;
}

.cyber-input:focus {
    border-color: rgba(176, 38, 255, 0.45) !important;

    box-shadow:
        0 0 10px rgba(176, 38, 255, 0.18) !important;
}

/* placeholder */
.cyber-input::placeholder {
    color: rgba(255,255,255,0.45);
}

/* option */
.cyber-input option {
    background: #121a2a;
    color: white;
}

/* =====================================================================================
   BOTON
===================================================================================== */
.cyber-btn {
    height: 50px;

    background: rgba(176, 38, 255, 0.15);

    border: 1px solid rgba(176, 38, 255, 0.35);

    color: white;

    transition: 0.3s;
}

.cyber-btn:hover {
    background: #b026ff;

    color: white;

    transform: translateY(-2px);

    box-shadow:
        0 0 12px rgba(176, 38, 255, 0.25);
}

/* =====================================================================================
   RESPONSIVE
===================================================================================== */
@media (max-width: 768px) {

    .hero-title {
        font-size: 1.8rem;
    }

    .hero-subtitle {
        font-size: 0.95rem;
    }

    .search-container {
        padding: 20px;
    }

}

</style>
