<script setup>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import { useRoute } from 'vue-router';
import { libroComposable } from '@/componsables/libroComponsable';
import { watchEffect } from 'vue';

const route = useRoute();

const {datos: libro, error: error} = libroComposable(route.params.id, route.params.slug);

// Manejo de errores:
watchEffect(() => {

    if(error.value){
        //console.log("Error con la api: " + error.value)
        window.location = '/error'
    }
});

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

                <div class="breadcumb-text text-center text-white">


                </div>

            </div>

        </div>

    </div>

</div>

<!-- =====================================================================================
     DETALLE
===================================================================================== -->
<section class="cyber-section" v-if="libro.data">

    <div class="container">

        <div class="row justify-content-center">

            <div class="col-12 col-xl-10">

                <!-- CARD PRINCIPAL -->
                <div class="resource-card">

                    <!-- IMAGEN -->
                    <div class="resource-image">

                        <img :src="libro.data?.imagen" :alt="libro.data?.nombre">

                    </div>

                    <!-- CONTENIDO -->
                    <div class="resource-content">

                        <!-- META -->
                        <div class="resource-meta">

                            <span>
                                <i class="fas fa-calendar-alt"></i>
                                {{ libro.data.fecha }}
                            </span>

                            <span>
                                <i class="fas fa-folder"></i>
                                {{ libro.data.categoria }}
                            </span>

                            <span>
                                <i class="fas fa-user"></i>
                                {{ libro.data.user }}
                            </span>

                        </div>

                        <!-- TITULO -->
                        <h2 class="resource-title">
                            {{ libro.data.nombre }}
                        </h2>

                        <!-- DESCRIPCIÓN -->
                        <div class="resource-description">

                            <p>
                                {{ libro.data.descripcion }}
                            </p>

                        </div>

                        <!--RECURSO EN PDF-->
                        <div class="resource-description">
                            <a :href="libro.data.libro" target="_blank">
                                <h6 class="resource-description" style="color: #fff;">
                                    Link para leer el libro: {{ libro.data.nombre }}
                                </h6>
                            </a>
                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>

<Footer></Footer>

</template>

<style scoped>



/* =====================================================================================
   HERO
===================================================================================== */
.hero-title {
    font-size: 2.5rem;
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
   CARD PRINCIPAL
===================================================================================== */
.resource-card {
    background: #121a2a;

    border: 1px solid rgba(176, 38, 255, 0.12);

    border-radius: 22px;

    overflow: hidden;

    box-shadow:
        0 0 20px rgba(176, 38, 255, 0.08);
}

/* =====================================================================================
   IMAGEN
===================================================================================== */
.resource-image img {
    width: 100%;

    height: 450px;

    object-fit: cover;

    display: block;
}

/* =====================================================================================
   CONTENIDO
===================================================================================== */
.resource-content {
    padding: 40px;
}

/* =====================================================================================
   META INFO
===================================================================================== */
.resource-meta {
    display: flex;

    flex-wrap: wrap;

    gap: 20px;

    margin-bottom: 25px;
}

.resource-meta span {
    color: rgba(255,255,255,0.65);

    font-size: 0.95rem;

    display: flex;
    align-items: center;
    gap: 8px;
}

.resource-meta i {
    color: #b026ff;
}

/* =====================================================================================
   TITULO
===================================================================================== */
.resource-title {
    color: white;

    font-size: 2rem;
    font-weight: 700;

    margin-bottom: 25px;
}

/* =====================================================================================
   DESCRIPCIÓN
===================================================================================== */
.resource-description p {
    color: rgba(255,255,255,0.72);

    line-height: 1.9;

    margin-bottom: 20px;
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

    .resource-image img {
        height: 250px;
    }

    .resource-content {
        padding: 25px;
    }

    .resource-title {
        font-size: 1.5rem;
    }

    .resource-meta {
        flex-direction: column;
        gap: 10px;
    }

}

</style>
