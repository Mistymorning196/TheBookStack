<template>
    <main>
        <!--Nav bar for every page -->
        <div class="navbar">
            <h2>The Book Stack</h2>
            <div class="nav-parts">
                <!--Go to home page -->
                <router-link class="link" :to="{name: 'Home Page'}">Home</router-link>
                <!-- Go to User Books Page-->
                <router-link class="link" :to="{name: 'List Page'}">My Books</router-link>
                <!-- Go to Blog Page-->
                <router-link class="link" :to="{name: 'Blog Page'}">Blog</router-link>
                <!-- Go to Profile Page-->
                <router-link class="link" :to="{name: 'Profile Page'}">Profile</router-link>
                <!-- Logout -->
                <a href='http://localhost:8000/logout/'>Log Out</a>
            </div>
        </div>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});
</script>

<style scoped>
    main {
        background-color: #EFE0CB; /* Light background */
        font-family: Arial, Helvetica, sans-serif;
        min-height: 100vh;
        margin: 0;
        display: flex;
        flex-direction: column;
    }
    
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #542F2F; /* Dark red background for navbar */
        padding: 1rem 2rem; /* Spacing around navbar */
        color: white;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* Light shadow for navbar */
    }

    .navbar h2 {
        font-size: 1.8rem;
        margin: 0;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .nav-parts {
        display: flex;
        gap: 1rem; /* Space out the navigation links */
    }

    .nav-parts > .link, a {
        padding: 0.6em 1em;
        text-decoration: none;
        color: white;
        font-size: 1rem;
        border-radius: 5px; /* Rounded corners */
        background-color: #955D5C; /* Light red color for buttons */
        border: none;
        font-weight: 500;
        transition: all 0.3s ease; /* Smooth transition on hover */
    }

    .nav-parts > .link:hover, a:hover {
        background-color: #723a39; /* Darker red on hover */
        color: #f8f8f8; /* Light text color for contrast */
        transform: scale(1.05); /* Slightly enlarge on hover */
    }

    /* Active state for router-links (optional) */
    .nav-parts > .link.router-link-exact-active {
        background-color: #6f3d3d; /* Darker red for active link */
    }

    .nav-parts > .link.router-link-exact-active:hover {
        background-color: #723a39; /* Darker hover for active link */
    }
</style>
