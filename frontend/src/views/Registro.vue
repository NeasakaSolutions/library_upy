<script setup>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import { ref } from 'vue';
import { registroComposable } from '@/componsables/useSeguridadComponsable';
import { ErrorMessage, Field, Form } from 'vee-validate';
import { registroSchema } from '@/schemas/validacionesSchema';

// Variables:
const boton = ref('block');
const preloader = ref('none');

const nombre = ref('');
const correo = ref('');
const password = ref('');

const { sendData } = registroComposable();

const enviar = async () => {
    boton.value = 'none';
    preloader.value = 'block';

    try {
        await sendData({
            nombre: nombre.value,
            correo: correo.value,
            password: password.value
        });
    } finally {
        boton.value = 'block';
        preloader.value = 'none';
    }
};
</script>

<template>
    <Header />

    <!-- =====================================================================================
         REGISTRO
    ====================================================================================== -->
    <section class="cyber-section">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-12 col-md-10 col-lg-7 col-xl-5">

                    <div class="login-card">

                        <!-- TITULO -->
                        <div class="text-center mb-4">
                            <h3 class="login-title">
                                Crear una cuenta
                            </h3>

                            <p class="login-subtitle">
                                Regístrate para solicitar acceso a la biblioteca virtual.
                            </p>
                        </div>

                        <!-- FORM -->
                        <Form
                            :validation-schema="registroSchema"
                            @submit="enviar"
                        >

                            <!-- NOMBRE -->
                            <div class="mb-4">
                                <ErrorMessage
                                    name="nombre"
                                    class="text text-danger"
                                />

                                <label class="form-label cyber-label">
                                    Nombre completo
                                </label>

                                <Field
                                    type="text"
                                    name="nombre"
                                    v-model="nombre"
                                    class="form-control cyber-input"
                                    placeholder="Ingresa tu nombre"
                                />
                            </div>

                            <!-- EMAIL -->
                            <div class="mb-4">
                                <ErrorMessage
                                    name="correo"
                                    class="text text-danger"
                                />

                                <label class="form-label cyber-label">
                                    Correo electrónico
                                </label>

                                <Field
                                    type="email"
                                    name="correo"
                                    v-model="correo"
                                    class="form-control cyber-input"
                                    placeholder="ejemplo@correo.com"
                                />
                            </div>

                            <!-- PASSWORD -->
                            <div class="mb-4">
                                <ErrorMessage
                                    name="password"
                                    class="text text-danger"
                                />

                                <label class="form-label cyber-label">
                                    Contraseña
                                </label>

                                <Field
                                    type="password"
                                    name="password"
                                    v-model="password"
                                    class="form-control cyber-input"
                                    placeholder="Crea una contraseña"
                                />
                            </div>

                            <!-- BUTTON -->
                            <div
                                class="d-grid"
                                v-if="boton === 'block'"
                            >
                                <button
                                    type="submit"
                                    class="btn cyber-btn"
                                    title="Registrarse"
                                >
                                    <i class="fas fa-user-plus me-2"></i>
                                    Crear cuenta
                                </button>
                            </div>

                            <!-- PRELOADER -->
                            <div
                                class="d-grid text-center"
                                v-if="preloader === 'block'"
                            >
                                <img
                                    src="/img/img/load.gif"
                                    class="mx-auto"
                                    width="70"
                                    alt="Cargando"
                                >
                                <p class="login-subtitle mt-2">
                                    Enviando solicitud...
                                </p>
                            </div>

                        </Form>

                        <!-- ENLACE A LOGIN -->
                        <div class="text-center mt-4">
                            <p class="login-subtitle">
                                ¿Ya tienes una cuenta?
                            </p>

                            <RouterLink
                                to="/login"
                                class="cyber-link"
                            >
                                Inicia sesión aquí
                            </RouterLink>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </section>

    <Footer />
</template>

<style scoped>
:global(body) {
    background: #0b0f1a;
    margin: 0;
    padding-top: 40px;
}

/* =====================================================================================
   SECCION
===================================================================================== */
.cyber-section {
    padding: 40px 0;
    min-height: 70vh;
    display: flex;
    align-items: center;
}

/* =====================================================================================
   TARJETA
===================================================================================== */
.login-card {
    background: #121a2a;
    border: 1px solid rgba(176, 38, 255, 0.12);
    border-radius: 22px;
    padding: 40px;
    box-shadow: 0 0 20px rgba(176, 38, 255, 0.08);
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
    color: rgba(255, 255, 255, 0.65);
    margin: 0;
    line-height: 1.7;
}

/* =====================================================================================
   LABELS
===================================================================================== */
.cyber-label {
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 10px;
    font-size: 0.95rem;
}

/* =====================================================================================
   INPUTS
===================================================================================== */
.cyber-input {
    height: 52px;
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: white !important;
    border-radius: 12px;
    padding: 0 16px;
}

.cyber-input:focus {
    border-color: rgba(176, 38, 255, 0.45) !important;
    box-shadow: 0 0 12px rgba(176, 38, 255, 0.15) !important;
}

.cyber-input::placeholder {
    color: rgba(255, 255, 255, 0.4);
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
    box-shadow: 0 0 15px rgba(176, 38, 255, 0.25);
}

/* =====================================================================================
   ENLACE
===================================================================================== */
.cyber-link {
    display: inline-block;
    margin-top: 8px;
    color: #c9a7ff;
    text-decoration: none;
    transition: 0.3s;
}

.cyber-link:hover {
    color: #8ecbff;
    text-shadow: 0 0 10px rgba(142, 203, 255, 0.35);
}

/* =====================================================================================
   RESPONSIVE
===================================================================================== */
@media (max-width: 768px) {
    .cyber-section {
        padding: 25px 0;
    }

    .login-card {
        padding: 28px;
    }

    .login-title {
        font-size: 1.6rem;
    }
}
</style>