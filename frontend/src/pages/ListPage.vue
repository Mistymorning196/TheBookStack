<template>
  <ReaderNavBarComponent />
  <section>
    <h2>Your Books:</h2>
  </section>
  <h3>Currently Reading</h3>
  <section class="display">
    <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'READING' && book.user === reader_id)" :key="index">
      <router-link :to="`/book/${userBook.book}`" class="book-link">
        <div v-if="userBook.cover_image">
          <img :src="`http://localhost:8000/${userBook.cover_image}`" alt="Book Cover" class="book-cover"/>
        </div>
        <p v-else>No cover image available</p>
        <p class="book-title">Title: {{ userBook.title }}</p>
        <p class="book-author">Author: {{ userBook.author }}</p>
      </router-link>
      <button @click="updateUserBookStatus(userBook, 'COMPLETED')">Completed</button>
      <button @click="deleteUserBook(userBook.id)">Delete</button>
    </div>
  </section>
  <h3>WishList</h3>
  <section class="display">
    <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'WISHLIST' && book.user === reader_id)" :key="index">
      <router-link :to="`/book/${userBook.book}`" class="book-link">
        <div v-if="userBook.cover_image">
          <img :src="`http://localhost:8000/${userBook.cover_image}`" alt="Book Cover" class="book-cover"/>
        </div>
        <p class="book-title">Title: {{ userBook.title }}</p>
        <p class="book-author">Author: {{ userBook.author }}</p>
      </router-link>
      <button @click="updateUserBookStatus(userBook, 'READING')">Reading</button>
      <button @click="deleteUserBook(userBook.id)">Delete</button>
    </div>
  </section>
  <h3>Completed</h3>
  <section class="display">
    <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'COMPLETED' && book.user === reader_id)" :key="index">
      <router-link :to="`/book/${userBook.book}`" class="book-link">
        <div v-if="userBook.cover_image">
          <img :src="`http://localhost:8000/${userBook.cover_image}`" alt="Book Cover" class="book-cover"/>
        </div>
        <p class="book-title">Title: {{ userBook.title }}</p>
        <p class="book-author">Author: {{ userBook.author }}</p>
      </router-link>
      <button @click="deleteUserBook(userBook.id)">Delete</button>
    </div>
  </section>
</template>

<script lang="ts">
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { defineComponent } from "vue";
import { useCookies } from "vue3-cookies";
import { useBooksStore } from "../stores/books.ts";
import { useUserBooksStore } from "../stores/userBooks.ts";
import { useReadersStore } from "../stores/readers.ts";
import { BookGenre, ReaderGenre, UserBook } from "../types"; 


export default defineComponent({
  data() {
    return {
      reader_id: Number(window.sessionStorage.getItem("reader_id")),
    };
  },
  async mounted() {
    const readerRes = await fetch("http://localhost:8000/readers/");
    const readerData = await readerRes.json();
    useReadersStore().saveReaders(readerData.users);

    const bookRes = await fetch("http://localhost:8000/books/");
    const bookData = await bookRes.json();
    useBooksStore().saveBooks(bookData.books);

    const userBookRes = await fetch("http://localhost:8000/user_books/");
    const userBookData = await userBookRes.json();
    useUserBooksStore().saveUserBooks(userBookData.user_books);
  },
  components: {
    ReaderNavBarComponent,
  },
  methods: {
    async updateUserBookStatus(userBook: UserBook, newStatus: string) {
      console.log('updateUserBookStatus triggered', userBook, newStatus);

      try {
        const { cookies } = useCookies();
        const response = await fetch(`http://localhost:8000/user_book/${userBook.id}/`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify({ status: newStatus }),
        });

        if (response.ok && newStatus === "COMPLETED") {
          const userRes = await fetch(`http://localhost:8000/reader/${this.reader_id}/`);
          const userData = await userRes.json();
          await fetch(`http://localhost:8000/reader/${this.reader_id}/`, {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${cookies.get("access_token")}`,
              "Content-Type": "application/json",
              "X-CSRFToken": cookies.get("csrftoken"),
            },
            credentials: "include",
            body: JSON.stringify({ book_count: userData.book_count + 1 }),
          });

          // Fetch and filter book genres
          const bookGenreRes = await fetch(`http://localhost:8000/book_genres/`);
          const bookGenreData = await bookGenreRes.json();
          const bookGenres: BookGenre[] = bookGenreData.book_genre || []; // Ensure it's typed as BookGenre[]

          const bookGenresForBook = bookGenres.filter((bg: BookGenre) => bg.book === userBook.book); // Explicitly type bg

          console.log('Filtered Book Genres:', bookGenresForBook);

          const readerGenreRes = await fetch(`http://localhost:8000/reader_genres/`);
          const readerGenreData = await readerGenreRes.json();
          const readerGenres = readerGenreData.reader_genre || [];

          for (const bg of bookGenresForBook) {
            const existing = readerGenres.find((rg: ReaderGenre) => rg.user === this.reader_id && rg.genre === bg.genre);

            if (existing) {
              await fetch(`http://localhost:8000/reader_genre/${existing.id}/`, {
                method: "PUT",
                headers: {
                  Authorization: `Bearer ${cookies.get("access_token")}`,
                  "Content-Type": "application/json",
                  "X-CSRFToken": cookies.get("csrftoken"),
                },
                credentials: "include",
                body: JSON.stringify({ count: existing.count + 1 }),
              });
            } else {
              await fetch(`http://localhost:8000/reader_genres/`, {
                method: "POST",
                headers: {
                  Authorization: `Bearer ${cookies.get("access_token")}`,
                  "Content-Type": "application/json",
                  "X-CSRFToken": cookies.get("csrftoken"),
                },
                credentials: "include",
                body: JSON.stringify({
                  user_id: this.reader_id,
                  genre_id: bg.genre,
                }),
              });
            }
          }
        }

        window.location.reload();
      } catch (error) {
        console.error("Failed to update book status:", error);
      }
    },

    async deleteUserBook(userBookId: number) {
      try {
        const { cookies } = useCookies();
        const userBook = this.userBooks.find(book => book.id === userBookId);

        const response = await fetch(`http://localhost:8000/user_book/${userBookId}/`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
        });

        if (response.ok && userBook?.status === "COMPLETED") {
          const userRes = await fetch(`http://localhost:8000/reader/${this.reader_id}/`);
          const userData = await userRes.json();
          await fetch(`http://localhost:8000/reader/${this.reader_id}/`, {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${cookies.get("access_token")}`,
              "Content-Type": "application/json",
              "X-CSRFToken": cookies.get("csrftoken"),
            },
            credentials: "include",
            body: JSON.stringify({ book_count: Math.max(userData.book_count - 1, 0) }),
          });

          const bookGenreRes = await fetch(`http://localhost:8000/book_genres/`);
          const bookGenreData = await bookGenreRes.json();
          const bookGenres: BookGenre[] = bookGenreData.book_genre || [];

          const readerGenreRes = await fetch(`http://localhost:8000/reader_genres/`);
          const readerGenreData = await readerGenreRes.json();
          const readerGenres = readerGenreData.reader_genre || [];

          const bookGenresForBook = bookGenres.filter((bg: BookGenre) => bg.book === userBook.book);

          for (const bg of bookGenresForBook) {
            const existing = readerGenres.find((rg: ReaderGenre) => rg.user === this.reader_id && rg.genre === bg.genre);
            if (existing) {
              const newCount = existing.count - 1;
              if (newCount <= 0) {
                await fetch(`http://localhost:8000/reader_genre/${existing.id}/`, {
                  method: "DELETE",
                  headers: {
                    Authorization: `Bearer ${cookies.get("access_token")}`,
                    "Content-Type": "application/json",
                    "X-CSRFToken": cookies.get("csrftoken"),
                  },
                  credentials: "include",
                });
              } else {
                await fetch(`http://localhost:8000/reader_genre/${existing.id}/`, {
                  method: "PUT",
                  headers: {
                    Authorization: `Bearer ${cookies.get("access_token")}`,
                    "Content-Type": "application/json",
                    "X-CSRFToken": cookies.get("csrftoken"),
                  },
                  credentials: "include",
                  body: JSON.stringify({ count: newCount }),
                });
              }
            }
          }
        }

        window.location.reload();
      } catch (error) {
        console.error("Error deleting user book relationship:", error);
        alert("Failed to delete user book relationship.");
      }
    },
  },
  computed: {
    books() {
      return useBooksStore().books;
    },
    userBooks() {
      return useUserBooksStore().userBooks;
    },
  },
  setup() {
    return {
      storeBook: useBooksStore(),
      storeUserBook: useUserBooksStore(),
    };
  },
});

</script>

  
<style scoped>
/* Body Styling */
.body {
    font-family: 'Arial', Helvetica, sans-serif;
    background-color: #EFE0CB; /* Light background */
    min-height: 100vh;
    padding: 0.1rem; /* Further reduced padding */
    margin: 0;
}

/* Specific adjustments for h3 (for "Reading", "WishList", "Completed") */
h3 {
    font-size: 1.1rem; /* Smaller font size */
    margin-bottom: 0.2em; /* Reduced bottom margin */
    max-width: 80%; /* Limit width to make it more compact */
    text-align: center; /* Center the headings */
    margin-left: auto; /* Center horizontally */
    margin-right: auto; /* Center horizontally */
}



/* Section Titles Styling */
h2, h3 {
    background: linear-gradient(135deg, #542F2F, #955D5C); /* Gradient background */
    color: #ffffff; /* White text */
    padding: 0.2rem 0.5rem; /* Reduced padding */
    margin: 0.4em 0; /* Reduced margins */
    border-radius: 8px; /* Slightly reduced border-radius */
    font-size: 1.3rem; /* Smaller font size for better fit */
    font-weight: bold;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2); /* Subtle text shadow */
    border-bottom: 3px solid #955D5C;
    position: relative;
    display: inline-block;
    width: auto; /* Reduce width of headings */
}



/* Smaller h2 */
h2 {
    font-size: 1.5rem; /* Reduced font size */
    margin-top: 0.8em; /* Reduced top margin */
}

/* Smaller h3 */
h3 {
    font-size: 1.1rem; /* Reduced font size */
    margin-bottom: 0.2em; /* Reduced bottom margin */
}

/* General Display Section Styling */
.display {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem; /* Reduced space between items */
    justify-content: start;
}

/* Book Card Styling */
.display > div {
    background-color: #2f4a54; /* Book container background */
    padding: 0.5rem; /* Reduced padding */
    margin: 0.2rem; /* Further reduced margin */
    border-radius: 8px; /* Slightly reduced border-radius */
    flex-basis: 28%; /* Adjusted width of each item */
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2); /* Slightly lighter shadow */
    transition: all 0.3s ease-in-out;
    max-height: 180px; /* Further reduced max height */
    overflow: hidden; /* Hide overflow */
}

/* Book Card Hover Effect */
.display > div:hover {
    transform: translateY(-4px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3); /* Elevated effect */
}

/* Book Link Styling */
.book-link {
    text-decoration: none;
    color: white;
    font-size: 0.9rem; /* Smaller font size */
    font-weight: bold;
    transition: all 0.3s ease;
}

/* Book Link Hover Effect */
.book-link:hover {

    transform: scale(1.05);
}

/* Book Title Styling */
.book-title {
    background-color: #71929f; /* Lighter background for title */
    padding: 0.3em; /* Reduced padding */
    margin: 0.2em 0; /* Reduced margin */
    border-radius: 5px;
    font-weight: bold;
    font-size: 1rem; /* Slightly smaller font size */
}

/* Book Author Styling */
.book-author {
    background-color: #71929f; /* Lighter background for author */
    padding: 0.3em; /* Reduced padding */
    margin: 0.2em 0; /* Reduced margin */
    border-radius: 5px;
    font-size: 1rem; /* Adjusted font size */
    color: #c1d3d9; /* Soft color for author */
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


/* Responsive Layout for Smaller Screens */
@media (max-width: 768px) {
    .display {
        flex-direction: column;
        align-items: center;
    }

    .display > div {
        flex-basis: 100%; /* Stack items on smaller screens */
        max-height: none; /* Remove max height */
    }

    h2, h3 {
        font-size: 1.1rem; /* Reduced heading size */
        width: 90%; /* Reduced width of headings */
    }
}


</style>


  