<template>
  <AuthorNavBarComponent />

  <h2>Books:</h2>
  <div class="scroll-container">
    <section class="display">
      <div v-for="(authorBook, index) in authorBooks.filter(book => book.user === reader_id)" :key="index">
        <router-link :to="`/authorBook/${authorBook.book}`" class="book-link">
          <div v-if="authorBook.cover_image">
            <img :src="`https://thebookstack-2.onrender.com/${authorBook.cover_image}`" alt="Book Cover" class="book-cover"/>
          </div>
          <p v-else>No cover image available</p>
          <p class="book-title">Title: {{ authorBook.title }}</p>
          <p class="book-author">Author: {{ authorBook.author }}</p>
        </router-link>
        <button class="delete-btn" @click="deleteBook(authorBook.book)">Delete</button>
      </div>
    </section>
  </div>
  <router-link :to="`/addBook/`" class="book-link">Add Book</router-link>

  <h2>Blog Posts:</h2>
  <div class="scroll-container">
    <section class="display">
      <div v-for="(authorBlog, index) in authorBlogs.filter(blog => blog.user === reader_id)" :key="index">
        <router-link :to="`/authorPost/${authorBlog.blog}`" class="book-link">
          <p class="book-title">Title: {{ authorBlog.title }}</p>
          <p class="book-author">Author: {{ authorBlog.author }}</p>
        </router-link>
        <button class="delete-btn" @click="deleteBlog(authorBlog.blog)">Delete</button>
      </div>
    </section>
  </div>
  <router-link :to="`/addBlog/`" class="book-link">Add Blog</router-link>
</template>

<script lang="ts">
import {useCookies} from "vue3-cookies";
import { defineComponent } from "vue";
import AuthorNavBarComponent from "../components/AuthorNav.vue";
import { useAuthorBooksStore } from "../stores/authorBooks.ts";
import { useAuthorBlogsStore } from "../stores/authorBlogs.ts";
import { AuthorBook, AuthorBlog } from "../types/index.ts";

export default defineComponent({
  data() {
    return {
      reader_id: null as number | null,
    };
  },
  async mounted() {
    const sessionCookie = document.cookie.split(";");
    let currentSessionid = "";

    for (let cookie of sessionCookie) {
      cookie = cookie.trim();
      if (cookie.startsWith("sessionid=")) {
        currentSessionid = cookie.substring("sessionid=".length);
      }
    }

    const previousSessionid = window.sessionStorage.getItem("session_id");

    if (currentSessionid === previousSessionid) {
      this.reader_id = Number(window.sessionStorage.getItem("reader_id"));
    } else {
      const params = new URLSearchParams(window.location.search);
      this.reader_id = parseInt(params.get("u") || "0");
      sessionStorage.setItem("reader_id", this.reader_id.toString());
      sessionStorage.setItem("session_id", currentSessionid);
    }

    await this.fetchBooksAndBlogs();
  },
  components: {
    AuthorNavBarComponent,
  },
  methods: {
    async fetchBooksAndBlogs() {
      try {
        const responseAuthorBook = await fetch("https://thebookstack-2.onrender.com/author_books/");
        const dataAuthorBook = await responseAuthorBook.json();
        const authorBooks = dataAuthorBook.author_books as AuthorBook[];
        useAuthorBooksStore().saveAuthorBooks(authorBooks);

        const responseAuthorBlog = await fetch("https://thebookstack-2.onrender.com/author_blogs/");
        const dataAuthorBlog = await responseAuthorBlog.json();
        const authorBlogs = dataAuthorBlog.author_blogs as AuthorBlog[];
        useAuthorBlogsStore().saveAuthorBlogs(authorBlogs);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },

    async deleteBook(bookId: number) {
      if (!confirm("Are you sure you want to delete this book?")) return;

      try {
        const { cookies } = useCookies(); 
        const response = await fetch(`https://thebookstack-2.onrender.com/book/${bookId}/`, {
          method: "DELETE",
          headers: {
            "Authorization": `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
        });

        if (response.ok) {
          window.location.reload();
        } else {
          console.error("Failed to delete book");
        }
      } catch (error) {
        console.error("Error deleting book:", error);
      }
    },

    async deleteBlog(blogId: number) {
      if (!confirm("Are you sure you want to delete this blog post?")) return;

      try {
        const { cookies } = useCookies(); 
        const response = await fetch(`https://thebookstack-2.onrender.com/blog/${blogId}/`, {
          method: "DELETE",
          headers: {
            "Authorization": `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
        });

        if (response.ok) {
          window.location.reload();
        } else {
          console.error("Failed to delete blog post");
        }
      } catch (error) {
        console.error("Error deleting blog post:", error);
      }
    },
  },
  computed: {
    authorBooks() {
      return useAuthorBooksStore().authorBooks;
    },
    authorBlogs() {
      return useAuthorBlogsStore().authorBlogs;
    },
  },
});
</script>

<style scoped>
body {
  font-family: Arial, Helvetica, sans-serif;
  background-color: #efe0cb;
  margin: 0;
  padding: 0.5rem;
}

h1, h2 {
  color: white;
  background-color: #2f4a54;
  padding: 0.4rem 1rem;
  margin: 0.4rem 0;
  border-radius: 5px;
  font-size: 1.8rem;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.scroll-container {
  max-height: 250px;
  overflow-y: auto;
  margin-bottom: 0.5rem;
  padding: 0.3rem;
  background-color: #f4f1eb;
  border-radius: 6px;
  box-shadow: inset 0 0 4px rgba(0, 0, 0, 0.1);
}

.display {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  justify-content: flex-start;
  padding: 0.3rem;
}

.display > div {
  background-color: #2f4a54;
  padding: 0.4rem;
  border-radius: 6px;
  flex: 1 1 180px;
  max-width: 200px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.display > div:hover {
  transform: translateY(-2px);
}

.book-link, .blog-link {
  display: inline-block;
  background-color: #71929f;
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
  padding: 0.3rem 0.6rem;
  border-radius: 5px;
  text-align: center;
  text-decoration: none;
  margin: 0.4rem 0.2rem;
  transition: background-color 0.2s ease;
  max-width: 120px;
}

.book-link:hover, .blog-link:hover {
  background-color: #5d7e8b;
}

.book-link > p, .blog-link > p {
  margin: 0.1rem 0;
  padding: 0.2rem;
  background-color: #71929f;
  border-radius: 4px;
  color: white;
  text-align: center;
  font-size: 0.8rem;
}

.delete-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.75rem;
  margin-top: 0.3rem;
  width: 100%;
}

.delete-btn:hover {
  background-color: #c0392b;
}

.book-cover {
  width: 60px;           /* Smaller width */
  height: 60px;          /* Smaller height */
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
  margin-bottom: 0.3rem;
}

.book-cover:hover {
  transform: scale(1.03);
}


@media (max-width: 768px) {
  .display {
    flex-direction: column;
    align-items: center;
  }

  .display > div {
    flex-basis: 100%;
    max-width: 100%;
  }

  h1, h2 {
    font-size: 1.4rem;
  }

  .book-link, .blog-link {
    font-size: 0.75rem;
    padding: 0.3rem 0.5rem;
  }

  .book-link > p, .blog-link > p {
    font-size: 0.7rem;
  }
}
</style>

