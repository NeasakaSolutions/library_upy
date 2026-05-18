<script setup>
</script>

<template>

<div class="error-page">

    <div class="error-box">

        <h1 class="error-code">
            404
        </h1>

        <h2 class="error-title">
            Página no encontrada
        </h2>

        <p class="error-text">
            El recurso que intentas consultar no existe o fue movido.
        </p>

        <router-link to="/" class="error-button">
            Volver al inicio
        </router-link>

    </div>

</div>

</template>

<style scoped>

/* =====================================================================================
   CONTENEDOR GENERAL
===================================================================================== */
.error-page {
    min-height: 100vh;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #0b0f1a;

    padding: 20px;
}

/* =====================================================================================
   CAJA ERROR
===================================================================================== */
.error-box {
    width: 100%;
    max-width: 500px;

    text-align: center;

    background: #121a2a;

    border: 1px solid rgba(176, 38, 255, 0.2);

    border-radius: 18px;

    padding: 50px 35px;

    box-shadow:
        0 0 20px rgba(176, 38, 255, 0.12);
}

/* =====================================================================================
   404
===================================================================================== */
.error-code {
    font-size: 6rem;
    font-weight: 700;

    color: #b026ff;

    margin-bottom: 10px;

    text-shadow:
        0 0 15px rgba(176, 38, 255, 0.35);
}

/* =====================================================================================
   TITULO
===================================================================================== */
.error-title {
    color: white;

    font-size: 1.8rem;

    margin-bottom: 15px;
}

/* =====================================================================================
   TEXTO
===================================================================================== */
.error-text {
    color: rgba(255,255,255,0.65);

    line-height: 1.7;

    margin-bottom: 30px;
}

/* =====================================================================================
   BOTON
===================================================================================== */
.error-button {
    display: inline-block;

    padding: 12px 28px;

    border-radius: 10px;

    background: rgba(176, 38, 255, 0.15);

    border: 1px solid rgba(176, 38, 255, 0.35);

    color: white;

    text-decoration: none;

    transition: 0.3s;
}

.error-button:hover {
    background: #b026ff;

    color: white;

    transform: translateY(-2px);

    box-shadow:
        0 0 12px rgba(176, 38, 255, 0.35);
}

/* =====================================================================================
   RESPONSIVE
===================================================================================== */
@media (max-width: 768px) {

    .error-code {
        font-size: 4.5rem;
    }

    .error-title {
        font-size: 1.4rem;
    }

    .error-box {
        padding: 40px 25px;
    }
}

</style>