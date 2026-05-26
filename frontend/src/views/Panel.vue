<script setup>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import { onMounted, ref } from 'vue';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { librosSchema } from '@/schemas/validacionesSchema';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';

// Variables:
const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();
const route = useRoute();

const datos = ref({
    data: [],
    pagina_actual: 1,
    total_paginas: 1,
    total_registros: 0,
    hay_siguiente: false,
    hay_anterior: false
});

const categorias = ref([]);

// CONSULTAS
const getDatos = async (page = 1) => {
    const respuesta = await fetch(
        `${API_URL}libros-panel/${localStorage.getItem('libros_flaites_id')}?page=${page}`,
        {
            headers: {
                'content-type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('libros_flaites_token')}`
            }
        }
    );
    datos.value = await respuesta.json();

    const categorias_lista = await fetch(`${API_URL}categorias`, {
        headers: { 'content-type': 'application/json' }
    });
    categorias.value = await categorias_lista.json();
};

// PAGINACION
const cambiarPagina = async (pagina) => {
    if (pagina < 1 || pagina > datos.value.total_paginas) return;
    await getDatos(pagina);
};

// CARGA INICIAL
onMounted(() => {
    getDatos();
});

// Formulario recurso:
const nombre = ref('');
const autor = ref('');
const descripcion = ref('');
const categoria_id = ref('0');
const libros_id = ref('0');
const boton = ref('block');
const preloader = ref('none');

// INPUT FILES
const fotoInput = ref(null);
const libroInput = ref(null);

const slug = ref('');

// Mandar datos:
const enviar = async () => {
    try {
        boton.value = "none";
        preloader.value = "block";

        if (modal_titulo.value == "Crear") {

            const formData = new FormData();
            const foto = fotoInput.value.files[0];
            const libro = libroInput.value.files[0];

            formData.append('foto', foto);
            formData.append('libro', libro);
            formData.append('categoria_id', categoria_id.value);
            formData.append('nombre', nombre.value);
            formData.append('autor', autor.value);
            formData.append('descripcion', descripcion.value);

            await axios.post(
                `${API_URL}libros`,
                formData,
                {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('libros_flaites_token')}`
                    }
                }
            );

            alert("Registro exitoso.");
            await getDatos();
            document.querySelector('#resourceModal .btn-close').click();
        }

        if (modal_titulo.value == "Editar") {

            // 1. Actualizar datos básicos
            await axios.put(
                `${API_URL}libros/${libros_id.value}/${slug.value}`,
                {
                    nombre: nombre.value,
                    autor: autor.value,
                    descripcion: descripcion.value,
                    categoria_id: categoria_id.value
                },
                {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('libros_flaites_token')}`
                    }
                }
            );

            // Actualizar imagen si se selecciono una nueva
            if (fotoInput.value && fotoInput.value.files[0]) {
                const formDataFoto = new FormData();
                formDataFoto.append('foto', fotoInput.value.files[0]);
                formDataFoto.append('id', libros_id.value);

                await axios.post(
                    `${API_URL}libros/editar/foto`, 
                    formDataFoto,
                    {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('libros_flaites_token')}`
                        }
                    }
                );

                
            }

            // Libro PDF
            if (libroInput.value && libroInput.value.files[0]) {
                const formDataLibro = new FormData();
                formDataLibro.append('libro', libroInput.value.files[0]);
                formDataLibro.append('id', libros_id.value);

                await axios.post(
                    `${API_URL}libros/editar/documento`, 
                    formDataLibro,
                    {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('libros_flaites_token')}`
                        }
                    }
                ); 
            }

            alert("Modificación exitosa.");
            await getDatos();
            document.querySelector('#resourceModal .btn-close').click();
        }
    } catch (err) {
        console.log(err);
        console.log("Django dice:", err.response?.data);
        alert("Ocurrió un error.");
    } finally {
        boton.value = "block";
        preloader.value = "none";
    }
};

// Ventana modal:
const modal_titulo = ref('');

// Crear datos:
const crear = () => {
    modal_titulo.value = 'Crear';
    categoria_id.value = "0";
    nombre.value = '';
    autor.value = '';
    descripcion.value = '';
    preview_imagen.value = '';
    imagen_actual.value = '';
};

// Editar datos:
const editar = (modelo) => {
    modal_titulo.value = 'Editar';
    libros_id.value = modelo.id;
    slug.value = modelo.slug;
    categoria_id.value = modelo.categoria_id;
    nombre.value = modelo.nombre;
    autor.value = modelo.autor;
    descripcion.value = modelo.descripcion;
    imagen_actual.value = modelo.imagen;
    preview_imagen.value = '';

    if (fotoInput.value) fotoInput.value.value = '';
    if (libroInput.value) libroInput.value.value = '';
};

// Eliminar datos:
const eliminar = async (id, slug) => {
    if (!window.confirm("Confirmar eliminación.")) return;
    try {
        await axios.delete(`${API_URL}libros/${id}/${slug}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('libros_flaites_token')}`
            }
        });
        alert("Eliminación exitosa.");
        await getDatos();
    } catch (err) {
        console.log(err);
        alert("Ocurrió un error al eliminar.");
    }
};

// Editar foto:
const imagen_actual = ref('');
const preview_imagen = ref('');

onMounted(async () => {
    const id = route.params.id;
    if (!id) return;

    const respuesta = await fetch(`${API_URL}libros/${id}`, {
        headers: { 'content-type': 'application/json' }
    });

    if (respuesta.status != 200) {
        window.location = "/error";
    }

    datos.value = await respuesta.json();
});

// Preview de la foto:
const onFotoChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    preview_imagen.value = URL.createObjectURL(file);
};

const irDetalles = (id, slug) => {
    router.push({
        name: 'librosDetalle',
        params: { id, slug }
    });
};

// =====================================================================================
// CATEGORÍAS
// =====================================================================================
const nueva_categoria = ref('');
const boton_categoria = ref('block');
const preloader_categoria = ref('none');

const crearCategoria = async () => {
    if (!nueva_categoria.value.trim()) {
        alert("El nombre de la categoría no puede estar vacío.");
        return;
    }

    try {
        boton_categoria.value = "none";
        preloader_categoria.value = "block";

        await axios.post(
            `${API_URL}categorias`,
            { nombre: nueva_categoria.value.trim() },
            {
                headers: {
                    'content-type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('libros_flaites_token')}`
                }
            }
        );

        alert("Categoría creada exitosamente.");
        nueva_categoria.value = '';
        await getDatos(); // Refresca lista de categorías
        document.querySelector('#categoryModal .btn-close').click();

    } catch (err) {
        console.log(err);
        alert("Ocurrió un error al crear la categoría.");
    } finally {
        boton_categoria.value = "block";
        preloader_categoria.value = "none";
    }
};

const eliminarCategoria = async (id) => {
    if (!window.confirm("¿Confirmar eliminación de la categoría?")) return;

    try {
        await axios.delete(
            `${API_URL}categorias/${id}`,
            {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('libros_flaites_token')}`
                }
            }
        );

        alert("Categoría eliminada exitosamente.");
        await getDatos();

    } catch (err) {
        console.log(err);

        // Django devuelve 400 o 409 si hay libros asociados
        if (err.response && (err.response.status === 400 || err.response.status === 409)) {
            alert("No se puede eliminar la categoría porque tiene libros asociados.");
        } else {
            alert("Ocurrió un error al eliminar la categoría.");
        }
    }
};
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
                <div class="breadcumb-text text-center text-white"></div>
            </div>
        </div>
    </div>
</div>

<!-- =====================================================================================
     PANEL
===================================================================================== -->
<section class="cyber-section">

    <div class="container">

        <!-- HEADER -->
        <div class="panel-header">
            <div>
                <h3 class="panel-title">Mis recursos publicados</h3>
                <p class="panel-subtitle">Gestiona, edita y elimina contenido.</p>
            </div>

            <!-- BOTONES -->
            <div class="d-flex gap-3 flex-wrap">

                <!-- CREAR RECURSO -->
                <button
                    class="btn cyber-btn"
                    data-bs-toggle="modal"
                    data-bs-target="#resourceModal"
                    @click="crear"
                >
                    <i class="fas fa-plus me-2"></i>
                    Crear recurso
                </button>

                <!-- GESTIONAR CATEGORÍAS -->
                <button
                    class="btn cyber-btn"
                    data-bs-toggle="modal"
                    data-bs-target="#categoryModal"
                >
                    <i class="fas fa-folder-plus me-2"></i>
                    Gestionar categorías
                </button>

            </div>
        </div>

        <!-- =====================================================================================
             TABLA DESKTOP
        ===================================================================================== -->
        <div class="table-container d-none d-lg-block">
            <div class="table-responsive">
                <table class="table align-middle cyber-table">
                    <thead>
                        <tr>
                            <th>Categoría</th>
                            <th>Nombre</th>
                            <th>Autor</th>
                            <th>Descripción</th>
                            <th>Imagen</th>
                            <th class="text-center">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="(dato, index) in datos.data"
                            :key="index"
                            class="clickable-row"
                            @click="irDetalles(dato.id, dato.slug)"
                        >
                            <td>{{ dato.categoria }}</td>
                            <td>{{ dato.nombre }}</td>
                            <td>{{ dato.autor }}</td>
                            <td class="description-cell">{{ dato.descripcion }}</td>
                            <td>
                                <img :src="dato.imagen" class="table-image" :alt="dato.nombre">
                            </td>
                            <td class="text-center">
                                <button
                                    title="Editar"
                                    class="action-btn"
                                    data-bs-toggle="modal"
                                    data-bs-target="#resourceModal"
                                    @click.stop="editar(dato)"
                                >
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button
                                    title="Eliminar"
                                    class="action-btn delete-btn"
                                    @click.stop="eliminar(dato.id, dato.slug)"
                                >
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- =====================================================================================
             TARJETAS MOBILE
        ===================================================================================== -->
        <div class="d-lg-none">
            <div
                v-for="(dato, index) in datos.data"
                :key="index"
                class="mobile-card clickable-card"
                @click="irDetalles(dato.id, dato.slug)"
            >
                <img :src="dato.imagen" :alt="dato.nombre" class="mobile-image">
                <div class="mobile-content">
                    <span class="mobile-category">{{ dato.categoria }}</span>
                    <h5 class="mobile-title">{{ dato.nombre }}</h5>
                    <p class="mobile-time">{{ dato.tiempo }}</p>
                    <p class="mobile-description">{{ dato.descripcion }}</p>
                    <div class="mobile-actions">
                        <button
                            title="Editar"
                            class="action-btn"
                            data-bs-toggle="modal"
                            data-bs-target="#resourceModal"
                            @click.stop="editar(dato)"
                        >
                            <i class="fas fa-edit"></i>
                        </button>
                        <button
                            title="Eliminar"
                            class="action-btn delete-btn"
                            @click.stop="eliminar(dato.id, dato.slug)"
                        >
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>

    </div>

</section>

<!-- PAGINACION -->
<div class="row mt-5">
    <div class="col-12">
        <div class="d-flex justify-content-center align-items-center gap-2 flex-wrap">
            <button
                class="btn cyber-page-btn"
                :disabled="!datos.hay_anterior"
                @click="cambiarPagina(datos.pagina_actual - 1)"
            >
                Anterior
            </button>
            <button
                v-for="pagina in datos.total_paginas"
                :key="pagina"
                class="btn cyber-page-btn"
                :class="{ active: pagina === datos.pagina_actual }"
                @click="cambiarPagina(pagina)"
            >
                {{ pagina }}
            </button>
            <button
                class="btn cyber-page-btn"
                :disabled="!datos.hay_siguiente"
                @click="cambiarPagina(datos.pagina_actual + 1)"
            >
                Siguiente
            </button>
        </div>
    </div>
</div>

<!-- =====================================================================================
     MODAL RECURSO
===================================================================================== -->
<div class="modal fade" id="resourceModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content cyber-modal">

            <div class="modal-header cyber-modal-header">
                <h5 class="modal-title">{{ modal_titulo }} recurso</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>

            <div class="modal-body">
                <Form :validation-schema="librosSchema" @submit="enviar">
                    <div class="row g-4">

                        <!-- CATEGORIA -->
                        <div class="col-12">
                            <ErrorMessage name="categoria_id" class="text-danger d-block mb-2" />
                            <label class="cyber-label">Categoría</label>
                            <Field
                                as="select"
                                name="categoria_id"
                                v-model="categoria_id"
                                class="form-select cyber-input"
                            >
                                <option value="0" disabled>Seleccione...</option>
                                <option
                                    v-for="(categoria, index) in categorias.data"
                                    :key="index"
                                    :value="categoria.id"
                                >
                                    {{ categoria.nombre }}
                                </option>
                            </Field>
                        </div>

                        <!-- NOMBRE -->
                        <div class="col-12">
                            <ErrorMessage name="nombre" class="text-danger d-block mb-2" />
                            <label class="cyber-label">Nombre</label>
                            <Field
                                type="text"
                                name="nombre"
                                v-model="nombre"
                                class="form-control cyber-input"
                                placeholder="Nombre del recurso"
                            />
                        </div>

                        <!-- AUTOR -->
                        <div class="col-12">
                            <ErrorMessage name="autor" class="text-danger d-block mb-2" />
                            <label class="cyber-label">Autor</label>
                            <Field
                                type="text"
                                name="autor"
                                v-model="autor"
                                class="form-control cyber-input"
                                placeholder="Autor"
                            />
                        </div>

                        <!-- DESCRIPCION -->
                        <div class="col-12">
                            <ErrorMessage name="descripcion" class="text-danger d-block mb-2" />
                            <label class="cyber-label">Descripción</label>
                            <Field
                                as="textarea"
                                name="descripcion"
                                v-model="descripcion"
                                class="form-control cyber-input cyber-textarea"
                                placeholder="Descripción..."
                            />
                        </div>

                        <!-- FOTO -->
                        <div class="col-12">
                            <label class="cyber-label">
                                Portada
                                <span v-if="modal_titulo === 'Editar'" class="optional-label">
                                    — opcional, solo si deseas cambiarla
                                </span>
                            </label>

                            <div v-if="modal_titulo === 'Editar'" class="mb-3">
                                <img
                                    :src="preview_imagen || imagen_actual"
                                    style="width: 300px; border-radius: 8px;"
                                    :alt="nombre"
                                />
                            </div>

                            <input
                                type="file"
                                name="foto"
                                accept="image/*"
                                class="form-control cyber-input"
                                ref="fotoInput"
                                @change="onFotoChange"
                            />
                        </div>

                        <!-- DOCUMENTO -->
                        <div class="col-12">
                            <label class="cyber-label">
                                Libro (PDF)
                                <span v-if="modal_titulo === 'Editar'" class="optional-label">
                                    — opcional, solo si deseas reemplazarlo
                                </span>
                            </label>
                            <input
                                type="file"
                                name="libro"
                                accept=".pdf"
                                class="form-control cyber-input"
                                ref="libroInput"
                            />
                        </div>

                        <!-- BOTON -->
                        <div class="col-12">
                            <button
                                type="submit"
                                class="btn cyber-btn w-100"
                                :style="'display:' + boton"
                            >
                                Guardar recurso
                            </button>
                            <div class="text-center" :style="'display:' + preloader">
                                <img src="/img/img/load.gif" width="60">
                            </div>
                        </div>

                    </div>
                </Form>
            </div>

        </div>
    </div>
</div>

<!-- =====================================================================================
     MODAL CATEGORIA
===================================================================================== -->
<div class="modal fade" id="categoryModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content cyber-modal">

            <div class="modal-header cyber-modal-header">
                <h5 class="modal-title">Gestionar categorías</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>

            <div class="modal-body">

                <!-- CREAR CATEGORÍA -->
                <div class="mb-4">
                    <label class="cyber-label">Nueva categoría</label>
                    <div class="d-flex gap-2">
                        <input
                            type="text"
                            class="form-control cyber-input"
                            placeholder="Ejemplo: Redes"
                            v-model="nueva_categoria"
                            @keyup.enter="crearCategoria"
                        />
                        <button
                            class="btn cyber-btn"
                            :style="'display:' + boton_categoria"
                            @click="crearCategoria"
                            style="white-space: nowrap;"
                        >
                            <i class="fas fa-plus me-1"></i> Agregar
                        </button>
                    </div>
                    <div class="text-center mt-2" :style="'display:' + preloader_categoria">
                        <img src="/img/img/load.gif" width="40">
                    </div>
                </div>

                <!-- LISTA DE CATEGORÍAS EXISTENTES -->
                <div v-if="categorias.data && categorias.data.length > 0">
                    <label class="cyber-label mb-3">Categorías existentes</label>
                    <div class="category-list">
                        <div
                            v-for="(cat, index) in categorias.data"
                            :key="index"
                            class="category-item"
                        >
                            <span class="category-name">
                                <i class="fas fa-folder me-2 category-icon"></i>
                                {{ cat.nombre }}
                            </span>
                            <button
                                class="action-btn delete-btn"
                                title="Eliminar categoría"
                                @click="eliminarCategoria(cat.id)"
                            >
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <p v-else class="text-center" style="color: rgba(255,255,255,0.4); margin-top: 10px;">
                    No hay categorías creadas aún.
                </p>

            </div>

        </div>
    </div>
</div>

<Footer></Footer>

</template>

<style scoped>

:global(body) {
    background: #0b0f1a;
    margin: 0;
    padding-top: 80px;
}

.clickable-row {
    cursor: pointer;
    transition: 0.3s;
}

.clickable-row:hover {
    background: rgba(176, 38, 255, 0.08) !important;
}

.clickable-card {
    cursor: pointer;
    transition: 0.3s;
}

.clickable-card:hover {
    transform: translateY(-4px);
    border-color: rgba(176, 38, 255, 0.4);
    box-shadow: 0 0 20px rgba(176, 38, 255, 0.15);
}

.cyber-page-btn {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(176, 38, 255, 0.25);
    color: white;
    min-width: 45px;
    transition: 0.3s;
}

.cyber-page-btn:hover {
    background: rgba(176, 38, 255, 0.2);
    border-color: #b026ff;
    color: white;
}

.cyber-page-btn.active {
    background: #b026ff;
    border-color: #b026ff;
    box-shadow: 0 0 12px rgba(176, 38, 255, 0.4);
}

.cyber-page-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* =====================================================================================
   PANEL HEADER
===================================================================================== */
.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 30px;
}

.panel-title {
    color: white;
    margin-bottom: 8px;
}

.panel-subtitle {
    color: rgba(255,255,255,0.6);
    margin: 0;
}

/* =====================================================================================
   TABLA
===================================================================================== */
.table-container {
    background: #1f232a;
    border: 1px solid rgba(176, 38, 255, 0.12);
    border-radius: 20px;
    overflow: hidden;
}

.cyber-table {
    margin: 0;
    color: white;
    --bs-table-bg: #1f232a;
    --bs-table-color: white;
    --bs-table-border-color: rgba(255,255,255,0.06);
    background: #1f232a;
}

.cyber-table thead {
    background: rgba(255,255,255,0.03);
}

.cyber-table th {
    color: white;
    border: none;
    padding: 18px;
    white-space: nowrap;
}

.cyber-table td {
    border-color: rgba(255,255,255,0.06);
    padding: 18px;
    vertical-align: middle;
}

.cyber-table td,
.cyber-table th {
    background: transparent !important;
}

.cyber-table tbody tr:hover {
    background: rgba(255,255,255,0.02);
}

.description-cell {
    min-width: 250px;
}

/* =====================================================================================
   IMAGEN TABLA
===================================================================================== */
.table-image {
    width: 90px;
    height: 60px;
    object-fit: cover;
    border-radius: 10px;
}

/* =====================================================================================
   MOBILE CARDS
===================================================================================== */
.mobile-card {
    background: #121a2a;
    border: 1px solid rgba(176, 38, 255, 0.12);
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 20px;
}

.mobile-image {
    width: 100%;
    height: 220px;
    object-fit: cover;
}

.mobile-content {
    padding: 20px;
}

.mobile-category {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 30px;
    background: rgba(176, 38, 255, 0.12);
    color: #d68cff;
    font-size: 0.8rem;
    margin-bottom: 12px;
}

.mobile-title {
    color: white;
    margin-bottom: 10px;
}

.mobile-time {
    color: #b026ff;
    margin-bottom: 12px;
    font-size: 0.9rem;
}

.mobile-description {
    color: rgba(255,255,255,0.65);
    line-height: 1.7;
    margin-bottom: 20px;
}

.mobile-actions {
    display: flex;
    gap: 12px;
}

/* =====================================================================================
   BOTONES
===================================================================================== */
.action-btn {
    width: 40px;
    height: 40px;
    border: none;
    border-radius: 10px;
    background: rgba(176, 38, 255, 0.12);
    color: #b026ff;
    transition: 0.3s;
    flex-shrink: 0;
}

.action-btn:hover {
    background: #b026ff;
    color: white;
}

.delete-btn {
    background: rgba(255, 80, 80, 0.12);
    color: #ff5757;
}

.delete-btn:hover {
    background: #ff5757;
    color: white;
}

/* =====================================================================================
   BOTON PRINCIPAL
===================================================================================== */
.cyber-btn {
    background: rgba(176, 38, 255, 0.15);
    border: 1px solid rgba(176, 38, 255, 0.35);
    color: white;
    padding: 12px 22px;
    border-radius: 12px;
    transition: 0.3s;
}

.cyber-btn:hover {
    background: #b026ff;
    color: white;
}

/* =====================================================================================
   MODAL
===================================================================================== */
.modal {
    z-index: 99999 !important;
}

.modal-dialog {
    margin-top: 100px;
}

.cyber-modal {
    background: #121a2a;
    border: 1px solid rgba(176, 38, 255, 0.18);
    border-radius: 22px;
    overflow: hidden;
}

.cyber-modal-header {
    border-bottom: 1px solid rgba(255,255,255,0.06);
    background: rgba(176, 38, 255, 0.05);
}

.modal-title {
    color: white;
}

/* =====================================================================================
   LABELS
===================================================================================== */
.cyber-label {
    color: rgba(255,255,255,0.8);
    margin-bottom: 10px;
    display: block;
}

.optional-label {
    color: rgba(255,255,255,0.4);
    font-size: 0.82rem;
    font-weight: 400;
}

/* =====================================================================================
   INPUTS
===================================================================================== */
.cyber-input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 12px;
    min-height: 50px;
}

.cyber-input:focus {
    border-color: rgba(176, 38, 255, 0.45) !important;
    box-shadow: 0 0 10px rgba(176, 38, 255, 0.15) !important;
}

.cyber-input::placeholder {
    color: rgba(255,255,255,0.4);
}

.cyber-input option {
    background: #121a2a;
}

.cyber-textarea {
    min-height: 140px;
    padding-top: 14px;
}

/* =====================================================================================
   LISTA DE CATEGORÍAS
===================================================================================== */
.category-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-height: 280px;
    overflow-y: auto;
    padding-right: 4px;
}

.category-list::-webkit-scrollbar {
    width: 4px;
}

.category-list::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.03);
    border-radius: 4px;
}

.category-list::-webkit-scrollbar-thumb {
    background: rgba(176, 38, 255, 0.35);
    border-radius: 4px;
}

.category-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    transition: 0.2s;
}

.category-item:hover {
    border-color: rgba(176, 38, 255, 0.25);
    background: rgba(176, 38, 255, 0.05);
}

.category-name {
    color: rgba(255,255,255,0.85);
    font-size: 0.95rem;
}

.category-icon {
    color: #b026ff;
}

/* =====================================================================================
   RESPONSIVE
===================================================================================== */
@media (max-width: 991px) {

    .panel-header {
        flex-direction: column;
        align-items: stretch;
    }

    .panel-title {
        font-size: 1.4rem;
    }

    .cyber-btn {
        width: 100%;
    }

    .modal-dialog {
        margin: 90px 12px;
    }

}
</style>