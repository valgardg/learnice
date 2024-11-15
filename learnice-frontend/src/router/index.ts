import { createRouter, createWebHistory } from "vue-router";
import Home from '../screens/Home.vue';
import About from '../screens/About.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/home'
        },
        { 
            path: '/home', 
            name: 'home',
            component: Home 
        },
        { 
            path: '/about',
            name: 'about',
            component: About 
        },
    ],
});

export default router;