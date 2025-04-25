<template>
  <ReaderNavBarComponent />
  <div class="body">
    <div id="profile-box">
      <h2>Author Info</h2>
      <p>Username: {{ author.username }}</p>
      <p>Name: {{ author.first_name }} {{ author.last_name }}</p>
      <p>Biography: {{ author.biography }}</p>
    </div>

    <div class="display-books">
      <h2>Books</h2>
      <div class="grid-scroll">
        <div
          v-for="(authorBook, index) in authorBooks.filter(book => book.user === author.id)"
          :key="index"
          class="grid-item"
        >
          <router-link :to="`/book/${authorBook.book}`" class="book-link">
            <div v-if="authorBook.cover_image">
              <img :src="`http://localhost:8000/${authorBook.cover_image}`" alt="Book Cover" class="book-cover"/>
            </div>
            <p v-else>No cover image available</p>
            <p class="book-title">Title: {{ authorBook.title }}</p>
            <p class="book-author">Author: {{ authorBook.author }}</p>
          </router-link>
        </div>
      </div>

      <h2>Blogs</h2>
      <div class="grid-scroll">
        <div
          v-for="(authorBlog, index) in authorBlogs.filter(blog => blog.user === author.id)"
          :key="index"
          class="grid-item"
        >
          <router-link :to="`/post/${authorBlog.blog}`" class="book-link">
            <p class="book-title">Title: {{ authorBlog.title }}</p>
            <p class="book-author">Author: {{ authorBlog.author }}</p>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { defineComponent } from "vue";
import { useRoute } from "vue-router";
import { Author, AuthorBlog, AuthorBook } from "../types";
import { useAuthorBooksStore } from "../stores/authorBooks.ts";
import { useAuthorBlogsStore } from "../stores/authorBlogs.ts";
import { useAuthorStore } from "../stores/author.ts";

export default defineComponent({
  data() {
    return {
      reader_id: Number(window.sessionStorage.getItem("reader_id")),
    };
  },
  async mounted() {
    const route = useRoute();
    const authorId = parseInt(route.params.id);
    await this.authorStore.fetchAuthorReturn(authorId);

    let responseAuthorBook = await fetch("http://localhost:8000/author_books/");
    let dataAuthorBook = await responseAuthorBook.json();
    const storeAuthorBook = useAuthorBooksStore();
    storeAuthorBook.saveAuthorBooks(dataAuthorBook.author_books);

    let responseAuthorBlog = await fetch("http://localhost:8000/author_blogs/");
    let dataAuthorBlog = await responseAuthorBlog.json();
    const storeAuthorBlog = useAuthorBlogsStore();
    storeAuthorBlog.saveAuthorBlogs(dataAuthorBlog.author_blogs);
  },
  components: {
    ReaderNavBarComponent,
  },
  computed: {
    author() {
      return this.authorStore.author;
    },
    authorBooks() {
      return this.storeAuthorBook.authorBooks;
    },
    authorBlogs() {
      return this.storeAuthorBlog.authorBlogs;
    },
  },
  setup() {
    const authorStore = useAuthorStore();
    const storeAuthorBook = useAuthorBooksStore();
    const storeAuthorBlog = useAuthorBlogsStore();
    return { authorStore, storeAuthorBook, storeAuthorBlog };
  },
});
</script>

<style scoped>
.body {
  font-family: Arial, Helvetica, sans-serif;
  display: flex;
  flex-wrap: wrap;
  gap: 1.5em;
  padding: 1.5em;
  background-color: #efe0cb;
}

/* Profile Box */
#profile-box {
  background-color: #2f4a54;
  color: white;
  padding: 1.5em;
  border-radius: 8px;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 300px;
  width: 100%;
}

#profile-box h2 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: white;
  border-bottom: 2px solid #71929f;
  padding-bottom: 0.4rem;
}

#profile-box p {
  font-size: 1rem;
  color: #cfd8dc;
  margin: 0.6rem 0;
}

.display-books {
  flex-grow: 1;
  background-color: #2f4a54;
  padding: 1.5em;
  border-radius: 8px;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
}

/* Section Titles */
h2 {
  background-color: #1e363f;
  padding: 0.6em;
  border-radius: 6px;
  color: white;
  text-align: center;
  margin-bottom: 1em;
  font-size: 1.1rem;
}

/* Scrollable Grid */
.grid-scroll {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1em;
  max-height: 200px;
  overflow-y: auto;
  padding: 0.5em;
  background-color: #2f4a54;
  border-radius: 8px;
}

.grid-item {
  background-color: #3b5d67;
  padding: 0.8em;
  border-radius: 6px;
  box-shadow: 1px 1px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease-in-out;
}

.grid-item:hover {
  transform: scale(1.02);
}

.book-link {
  display: block;
  text-decoration: none;
  color: white;
  font-size: 1rem;
  font-weight: bold;
}

.book-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
}

.book-author {
  font-size: 0.9rem;
  color: #cfd8dc;
}

.book-cover {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.2);
}
</style>

