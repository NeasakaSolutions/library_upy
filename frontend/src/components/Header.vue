<script setup>
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
                        <a class="nav-link" href="#">
                            Iniciar sesión
                        </a>
                    </li>

                </ul>

                <!-- BUSCADOR -->
                <form class="d-flex me-lg-3 my-2 my-lg-0 search-box">
                    <input
                        class="form-control search-input"
                        type="search"
                        placeholder="Buscar recursos..."
                        aria-label="Search"
                    />
                    <button class="btn btn-outline-light ms-2" type="submit">
                        <i class="fa fa-search"></i>
                    </button>
                </form>

            </div>

        </div>

    </nav>

</header>
</template>

<style scoped>


</style>