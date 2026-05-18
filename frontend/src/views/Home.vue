<script setup>
import Footer from '@/components/Footer.vue';
import Header from '@/components/Header.vue';
import { getDatosHome } from '@/services/homeService';
import { onMounted, ref } from 'vue';

let libros = ref([]); // Declarar variable de tipo reactiva

onMounted(async() => {

    libros.value = await getDatosHome();
});


</script>

<template>

    <Header></Header>

    <!-- HERO -->
    <div class="breadcumb-area bg-img cyber-hero"
        style="background-image: url('/img/bg-img/portada_home.jpeg')">

        <div class="container h-100">
            <div class="row h-100 align-items-center">
                <div class="col-12">

                    <div class="breadcumb-text text-center text-white px-3">

                    </div>

                </div>
            </div>
        </div>
    </div>

    <!-- LIBROS -->
    <section class="best-receipe-area cyber-section">
        <div class="container">

            <div class="row">
                <div class="col-12">
                    <div class="section-heading text-center">
                        <h3 style="color: white;">Últimos recursos publicados</h3>
                    </div>
                </div>
            </div>

            <div class="row g-4 mobile-spacing">

                <div v-for = "(libro, index) in libros.data" :key = "index" class="col-12 col-md-6 col-lg-4">
                    <router-link :to = "{name: 'librosDetalle', params:{id: libro.id, slug: libro.slug}}">
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

        </div>
    </section>

    <Footer></Footer>

</template>

<style scoped>

:global(body) {
    background: #0b0f1a;
    margin: 0;
}

</style>