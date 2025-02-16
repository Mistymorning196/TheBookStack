// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import HomePage from '../pages/HomePage.vue';
import BookPage from '../pages/BookPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import SearchPage from '../pages/SearchPage.vue';
import BlogPage from '../pages/BlogPage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Home Page', component: HomePage },
        { path: '/profile/', name: 'Profile Page', component: ProfilePage },
        { path: '/book/', name: 'Book Page', component: BookPage },
        { path: '/search/', name: 'Search Page', component: SearchPage },
        { path: '/blog/', name: 'BlogPage', component: BlogPage},
    ]
})

export default router
