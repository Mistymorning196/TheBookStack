<template>
  <ReaderNavBarComponent />
  <section>
    <h2>Your Books:</h2>
  </section>
    <!-- Users current books -->
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
        <!-- Change status and delete -->
      <button @click="updateUserBookStatus(userBook, 'COMPLETED')">Completed</button>
      <button @click="deleteUserBook(userBook.id)">Delete</button>
    </div>
  </section>
    <!-- Wishlist books -->
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
        <!-- Change status and delete-->
      <button @click="updateUserBookStatus(userBook, 'READING')">Reading</button>
      <button @click="deleteUserBook(userBook.id)">Delete</button>
    </div>
  </section>
    <!-- Complete books -->
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
        <!-- delete -->
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
    //fetch readers
    const readerRes = await fetch("http://localhost:8000/readers/");
    const readerData = await readerRes.json();
    useReadersStore().saveReaders(readerData.users);

    //fetch books
    const bookRes = await fetch("http://localhost:8000/books/");
    const bookData = await bookRes.json();
    useBooksStore().saveBooks(bookData.books);

    //fetch user books
    const userBookRes = await fetch("http://localhost:8000/user_books/");
    const userBookData = await userBookRes.json();
    useUserBooksStore().saveUserBooks(userBookData.user_books);
  },
  components: {
    ReaderNavBarComponent,
  },
  methods: {
    //update the status of the book  uisng put
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

        //if the status is updated to completed make reader genre relationships using book genres
        //these will be used to update recommendations
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
          const bookGenres: BookGenre[] = bookGenreData.book_genre || []; 

          const bookGenresForBook = bookGenres.filter((bg: BookGenre) => bg.book === userBook.book); 

          console.log('Filtered Book Genres:', bookGenresForBook);

          const readerGenreRes = await fetch(`http://localhost:8000/reader_genres/`);
          const readerGenreData = await readerGenreRes.json();
          const readerGenres = readerGenreData.reader_genre || [];

          //get all of the genres for the book
          for (const bg of bookGenresForBook) {
            const existing = readerGenres.find((rg: ReaderGenre) => rg.user === this.reader_id && rg.genre === bg.genre);

            //if the genre already has reader genre update count using put
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
            } 
            //or make a new reader genre using post
            else {
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

    //delete the relationship user book
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

        //if the status was completed delete reader genres so it doesn effect reader genre
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
    background-color: #EFE0CB; 
    min-height: 100vh;
    padding: 0.1rem; 
    margin: 0;
}

/* Specific adjustments for h3 (for "Reading", "WishList", "Completed") */
h3 {
    font-size: 1.1rem; 
    margin-bottom: 0.2em; 
    max-width: 80%; 
    text-align: center;
    margin-left: auto; 
    margin-right: auto; 
}



/* Section Titles Styling */
h2, h3 {
    background: linear-gradient(135deg, #542F2F, #955D5C); 
    color: #ffffff; 
    padding: 0.2rem 0.5rem; 
    margin: 0.4em 0; 
    border-radius: 8px; 
    font-size: 1.3rem; 
    font-weight: bold;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2); 
    border-bottom: 3px solid #955D5C;
    position: relative;
    display: inline-block;
    width: auto; 
}


h2 {
    font-size: 1.5rem; 
    margin-top: 0.8em;
}

h3 {
    font-size: 1.1rem;
    margin-bottom: 0.2em; 
}

/* General Display Section Styling */
.display {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem; 
    justify-content: start;
}

/* Book Card Styling */
.display > div {
    background-color: #2f4a54; 
    padding: 0.5rem; 
    margin: 0.2rem; 
    border-radius: 8px; 
    flex-basis: 28%;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2); 
    transition: all 0.3s ease-in-out;
    max-height: 180px; 
    overflow: hidden; 
}


.display > div:hover {
    transform: translateY(-4px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3); 
}

/* Book Link Styling */
.book-link {
    text-decoration: none;
    color: white;
    font-size: 0.9rem; 
    font-weight: bold;
    transition: all 0.3s ease;
}


.book-link:hover {

    transform: scale(1.05);
}

/* Book Title Styling */
.book-title {
    background-color: #71929f; 
    padding: 0.3em;
    margin: 0.2em 0; 
    border-radius: 5px;
    font-weight: bold;
    font-size: 1rem; 
}


.book-author {
    background-color: #71929f; 
    padding: 0.3em; 
    margin: 0.2em 0;
    border-radius: 5px;
    font-size: 1rem; 
    color: #c1d3d9; 
}

.book-cover {
  width: 60px;          
  height: 60px;          
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
        flex-basis: 100%; 
        max-height: none; 
    }

    h2, h3 {
        font-size: 1.1rem;
        width: 90%; 
    }
}


</style>


  