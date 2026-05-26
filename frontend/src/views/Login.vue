<script setup>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import { ref } from 'vue';
import { loginComposable } from '@/componsables/useSeguridadComponsable';
import { ErrorMessage, Field, Form } from 'vee-validate';
import { loginSchema } from '@/schemas/validacionesSchema';

// Variables:
const boton = ref('block');
const preloader = ref('none');
const correo = ref('');
const password = ref('');

const { sendData } = loginComposable()

let enviar = () => {

    boton.value = 'none';
    preloader.value = 'block';

    sendData({
        correo: correo.value,
        password: password.value
    });
}

</script>

<template>

<Header></Header>

<!-- =====================================================================================
     LOGIN
===================================================================================== -->
<section class="cyber-section">

    <div class="container">

        <div class="row justify-content-center">

            <div class="col-12 col-md-10 col-lg-7 col-xl-5">

                <div class="login-card">

                    <!-- TITULO -->
                    <div class="text-center mb-4">

                        <h3 class="login-title">
                            Ingresa tus datos
                        </h3>

                        <p class="login-subtitle">
                            Introduce tu correo y contraseña.
                        </p>

                    </div>

                    <!-- FORM -->
                    <Form :validation-schema="loginSchema" @submit="enviar()">

                        <!-- EMAIL -->
                        <div class="mb-4">

                            <ErrorMessage name="correo" class="text text-danger"/>

                            <label class="form-label cyber-label">
                                Correo electrónico
                            </label>

                            <Field type="text" name="correo" v-model="correo" class="form-control cyber-input"  placeholder="Correo"></Field>

                        </div>

                        <!-- PASSWORD -->
                        <div class="mb-4">

                            <ErrorMessage name="password" class="text text-danger"/>

                            <label class="form-label cyber-label">
                                Contraseña
                            </label>

                            <Field type="password" name="password" v-model="password" class="form-control cyber-input"  placeholder="contraseña"></Field>

                        </div>

                        <!-- BUTTON -->
                        <div class="d-grid" v-if="boton === 'block'">

                            <button
                                type="submit"
                                class="btn cyber-btn"
                                title="Enviar">

                                <i class="fas fa-lock me-2"></i>

                                Iniciar Sesión

                            </button>

                        </div>

                        <!-- PRELOADER -->
                        <div class="d-grid text-center" v-if="preloader === 'block'">

                            <img
                                src="/img/load.gif"
                                class="mx-auto"
                                width="70"
                                alt="Cargando">

                        </div>

                    </Form>

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
    padding-top: 40px;
}

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

    max-width: 650px;

    margin: auto;

    line-height: 1.7;
}

/* =====================================================================================
   LOGIN CARD
===================================================================================== */
.login-card {
    background: #121a2a;

    border: 1px solid rgba(176, 38, 255, 0.12);

    border-radius: 22px;

    padding: 40px;

    box-shadow:
        0 0 20px rgba(176, 38, 255, 0.08);
}

/* =====================================================================================
   TITULOS
===================================================================================== */
.login-title {
    color: white;

    font-size: 2rem;
    font-weight: 700;

    margin-bottom: 10px;
}

.login-subtitle {
    color: rgba(255,255,255,0.65);

    margin: 0;
}

/* =====================================================================================
   LABELS
===================================================================================== */
.cyber-label {
    color: rgba(255,255,255,0.8);

    margin-bottom: 10px;

    font-size: 0.95rem;
}

/* =====================================================================================
   INPUTS
===================================================================================== */
.cyber-input {
    height: 52px;

    background: rgba(255,255,255,0.05) !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    color: white !important;

    border-radius: 12px;

    padding: 0 16px;
}

.cyber-input:focus {
    border-color: rgba(176, 38, 255, 0.45) !important;

    box-shadow:
        0 0 12px rgba(176, 38, 255, 0.15) !important;
}

.cyber-input::placeholder {
    color: rgba(255,255,255,0.4);
}

/* =====================================================================================
   BOTON
===================================================================================== */
.cyber-btn {
    height: 52px;

    border-radius: 12px;

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
        0 0 15px rgba(176, 38, 255, 0.25);
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

    .login-card {
        padding: 28px;
    }

    .login-title {
        font-size: 1.6rem;
    }

}

</style>