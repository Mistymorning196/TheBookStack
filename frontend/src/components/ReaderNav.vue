<template>
    <div class="navbar">
      <h2>The Book Stack</h2>
  
      <!-- Toggle button for mobile -->
      <button class="menu-toggle" @click="toggleMenu">
        ☰
      </button>
  
       <!--Links for different parts of the web app -->
      <div class="nav-parts" :class="{ 'show-menu': isMenuOpen }">
        <router-link class="link" :to="{ name: 'Home Page' }">Home</router-link>
        <router-link class="link" :to="{ name: 'Search Page' }">Search</router-link>
        <router-link class="link" :to="{ name: 'List Page' }">My Books</router-link>
        <router-link class="link" :to="{ name: 'Blog Page' }">Blog</router-link>
        <router-link class="link" :to="{ name: 'Group Page' }">Groups</router-link>
        <router-link class="link" :to="{ name: 'Profile Page' }">Profile</router-link>
        <a href="http://localhost:8000/logout/">Log Out</a>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from "vue";
  
  export default defineComponent({
    name: "ReaderNavBarComponent",
    //for toggle menu
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
  /* Styles for navbar and buttons */
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #542f2f;
    padding: 1rem 2rem;
    color: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    flex-wrap: wrap;
    position: relative;
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
  
  .nav-parts > .link,
  .nav-parts > a {
    padding: 0.6em 1em;
    text-decoration: none;
    color: white;
    font-size: 1rem;
    border-radius: 5px;
    background-color: #955d5c;
    border: none;
    font-weight: 500;
    transition: all 0.3s ease;
  }
  
  .nav-parts > .link:hover,
  .nav-parts > a:hover {
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
s  

