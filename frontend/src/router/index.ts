// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import HomePage from '../pages/HomePage.vue';
import BookPage from '../pages/BookPage.vue';
import AddBookPage from '../pages/AddBookPage.vue';
import AddBlogPage from '../pages/AddBlogPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import SearchPage from '../pages/SearchPage.vue';
import BlogPage from '../pages/BlogPage.vue';
import MessagePage from '../pages/MessagePage.vue';
import ListPage from '../pages/ListPage.vue';
import UserPage from '../pages/UserPage.vue';
import AuthorHomePage from '../pages/AuthorHomePage.vue';
import AuthorProfilePage from '../pages/AuthorProfilePage.vue';
import AuthorBioPage from '../pages/AuthorBioPage.vue';
import AuthorBookPage from '../pages/AuthorBookPage.vue';
import PostPage from '../pages/PostPage.vue';
import AuthorPostPage from '../pages/AuthorPostPage.vue';
import AllBookPage from '../pages/AllBookPage.vue';
import GroupPage from '../pages/GroupPage.vue';
import DiscussionPage from '../pages/DiscussionPage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Home Page', component: HomePage },
        { path: '/authorHome/', name: 'Author Home Page', component: AuthorHomePage },
        { path: '/authorProfile/', name: 'Author Profile Page', component: AuthorProfilePage },
        { path: '/addBook/', name: 'Add Book Page', component: AddBookPage },
        { path: '/addBlog/', name: 'Add Blog Page', component: AddBlogPage },
        { path: '/profile/', name: 'Profile Page', component: ProfilePage },
        { path: '/book/:id', name: 'Book Page', component: BookPage },
        { path: '/allBooks/', name: 'All Book Page', component: AllBookPage },
        { path: '/authorBook/:id', name: 'Author Book Page', component: AuthorBookPage },
        { path: '/user/:id', name: 'User Page', component: UserPage },
        { path: '/authorBio/:id', name: 'AuthorBio Page', component: AuthorBioPage },
        { path: '/search/', name: 'Search Page', component: SearchPage },
        { path: '/blog/', name: 'Blog Page', component: BlogPage},
        { path: '/group/', name: 'Group Page', component: GroupPage},
        { path: '/post/:id', name: 'Post Page', component: PostPage},
        { path: '/discussion/:id', name: 'Discussion Page', component: DiscussionPage},
        { path: '/authorPost/:id', name: 'Author Post Page', component: AuthorPostPage},
        { path: '/message/:id', name: 'Message Page', component: MessagePage},
        { path: '/myBooks/', name: 'List Page', component: ListPage},
    ]
})

export default router
