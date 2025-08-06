import { useAuthStore } from '@/stores/useAuthStore'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Index.vue'),
      meta: {
        guestOnly: true
      }
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('@/views/Products.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/products/:id/edit',
      name: 'products.edit',
      component: () => import('@/views/Edit.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Auth/Login.vue'),
      meta: {
        guestOnly: true
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/Auth/Register.vue'),
      meta: {
        guestOnly: true
      }
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  // const authStore = useAuthStore()
  // const authUser = await authStore.getAuthUser()

  // if (to.meta.guestOnly && authUser) {
  //   next({ name: 'products' })
  // } else if (to.meta.requiresAuth && !authUser) {
  //   next({ name: 'login' })
  // } else {
    next()
  // }
})

export default router
