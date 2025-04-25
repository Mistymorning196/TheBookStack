<template>
    <main>
       
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
    
   
</style>
