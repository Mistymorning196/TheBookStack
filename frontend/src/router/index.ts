// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import HomePage from '../pages/HomePage.vue';
import BookPage from '../pages/BookPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import SearchPage from '../pages/SearchPage.vue';
import BlogPage from '../pages/BlogPage.vue';
import MessagePage from '../pages/MessagePage.vue';
import ListPage from '../pages/ListPage.vue';
import UserPage from '../pages/UserPage.vue';
import AuthorPage from '../pages/AuthorPage.vue';
import AuthorBioPage from '../pages/AuthorBioPage.vue';
import PostPage from '../pages/PostPage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Home Page', component: HomePage },
        { path: '/author/', name: 'Author Page', component: AuthorPage },
        { path: '/profile/', name: 'Profile Page', component: ProfilePage },
        { path: '/book/:id', name: 'Book Page', component: BookPage },
        { path: '/user/:id', name: 'User Page', component: UserPage },
        { path: '/authorBio/:id', name: 'AuthorBio Page', component: AuthorBioPage },
        { path: '/search/', name: 'Search Page', component: SearchPage },
        { path: '/blog/', name: 'Blog Page', component: BlogPage},
        { path: '/post/:id', name: 'Post Page', component: PostPage},
        { path: '/message/:id', name: 'Message Page', component: MessagePage},
        { path: '/myBooks/', name: 'List Page', component: ListPage},
    ]
})

export default router
