<template>
  <!--Nav bar for every page -->
  <div class="navbar">
    <h2>The Book Stack</h2>

    <!-- Toggle button for mobile -->
    <button class="menu-toggle" @click="toggleMenu">
      ☰
    </button>

    <div class="nav-parts" :class="{ 'show-menu': isMenuOpen }">
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
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "AuthorNavBarComponent",
  setup() {
    const isMenuOpen = ref(false);

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value;
    };

    return { isMenuOpen, toggleMenu };
  },
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

.menu-toggle {
  display: none;
  font-size: 1.5rem;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
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

/* Responsive Styles */
@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }

  .nav-parts {
    flex-direction: column;
    width: 100%;
    margin-top: 1rem;
    display: none;
  }

  /* The 'show-menu' class controls the visibility of the mobile menu */
  .nav-parts.show-menu {
    display: flex;
  }

  .nav-parts > .link,
  .nav-parts > a {
    width: 100%;
    text-align: center;
    background-color: #955d5c;
  }
}
</style>