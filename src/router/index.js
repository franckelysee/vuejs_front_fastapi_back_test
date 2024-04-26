import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RestaurantCardVue from '@/components/RestaurantCard.vue'
import RegisterVue from '../views/Register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '',
      name: 'home',
      component:()=> import("../views/login.vue")
    },
    {
      path: '/login',
      name: 'login',
      component:()=> import("../views/login.vue")

    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
      meta: {
        requiresAuth:true,
        role:['Role_admin']
      }
    },
    {
      path:"/register",
      name:"register",
      component: ()=> import("../views/Register.vue")
    }
  ]
})

export default router
