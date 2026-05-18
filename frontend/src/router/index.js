import Error404 from '@/views/Error404.vue'
import Libros from '@/views/Libros.vue'
import LibrosDetalle from '@/views/LibrosDetalle.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/views/Home.vue'),
      name: 'home'
    },
    {
      path: '/libros/detalle/:id/:slug',
      component: LibrosDetalle,
      name: 'librosDetalle'
    },
    {
      path: '/libros',
      component: Libros,
      name: 'libros'
    },
    {
      path: '/:pathMatch(.*)*',
      component: Error404,
    },
  ],
})

export default router
