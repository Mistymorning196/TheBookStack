<template>
    <main>
        <!--Nav bar for every page -->
        <div class="navbar">
       
                <h2>The Book Stack</h2>
                <div class="nav-parts">
                      <!--Go to home page -->
                    <router-link
                        class="link"
                        :to="{name: 'Home Page'}"
                    >
                        Home
                    </router-link>
                      <!-- Go to Profile Page-->
                    <router-link
                        class="link"
                        :to="{name: 'Profile Page'}"
                    >
                        Profile
                    </router-link>

                    <!-- Logout -->
                    <a href= 'http://localhost:8000/logout/'>Log Out</a>
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
  <!--Styling for page and navbar mainly colour and positions-->
<style scoped>
    main{
        background-color: #EFE0CB;;
        font-family: Arial, Helvetica, sans-serif;
    }
    
    .navbar{
        display: flex;
        background-color: #542F2F;
        padding-left: 0.5rem;
        color: white;
    }

    .nav-parts{
        display:flex;
    }

    .nav-parts > .link, a{
        padding: 0.5em;
        text-decoration: none;
        margin: 1em;
        color: white;
        font-size: 1rem;
        border-style: ridge;
        background-color: #955D5C;
        border: none;
    }
</style>