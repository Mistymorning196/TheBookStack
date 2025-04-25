<template>
    <!--Nav bar for every page -->
    <div class="navbar">
        <h2>The Book Stack</h2>
        <div class="nav-parts">
            <!--Go to home page -->
            <router-link class="link" :to="{name: 'Author Home Page'}">Home</router-link>
            <!--Go to home page -->
            <router-link class="link" :to="{name: 'Author Profile Page'}">Profile</router-link>
            <!-- Logout -->
            <a href='http://localhost:8000/logout/'>Log Out</a>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "AuthorNavBarComponent"
});
</script>

<style scoped>
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #542F2F;
        padding: 1rem 2rem;
        color: white;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }

    .navbar h2 {
        font-size: 1.8rem;
        margin: 0;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .nav-parts {
        display: flex;
        gap: 1rem;
    }

    .nav-parts > .link, a {
        padding: 0.6em 1em;
        text-decoration: none;
        color: white;
        font-size: 1rem;
        border-radius: 5px;
        background-color: #955D5C;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .nav-parts > .link:hover, a:hover {
        background-color: #723a39;
        color: #f8f8f8;
        transform: scale(1.05);
    }

    .nav-parts > .link.router-link-exact-active {
        background-color: #6f3d3d;
    }

    .nav-parts > .link.router-link-exact-active:hover {
        background-color: #723a39;
    }
</style>

