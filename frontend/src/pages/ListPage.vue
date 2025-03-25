<template>
    <section>
        <h2>Your Books:</h2>
    </section>
    <h3>Currently Reading</h3>
    <section class="display">
        <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'READING' && book.user === reader_id)" :key="index">
            <router-link :to="`/book/${userBook.book}`" class="book-link">
                <p class="book-title">Title: {{ books[userBook.book - 1]?.title }}</p>
                <p class="book-author">Author: {{ books[userBook.book - 1]?.author }}</p>
            </router-link>
            <button @click="updateUserBookStatus(userBook, 'COMPLETED')">Completed</button>
            <button @click="deleteUserBook(userBook.id)">Delete</button>
        </div>
    </section>
    <h3>WishList</h3>
    <section class="display">
        <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'WISHLIST' && book.user === reader_id)" :key="index">
            <router-link :to="`/book/${userBook.book}`" class="book-link">
                <p class="book-title">Title: {{ books[userBook.book - 1]?.title }}</p>
                <p class="book-author">Author: {{ books[userBook.book - 1]?.author }}</p>
            </router-link>
            <button @click="updateUserBookStatus(userBook, 'READING')">Reading</button>
            <button @click="deleteUserBook(userBook.id)">Delete</button>
        </div>
    </section>
    <h3>Completed</h3>
    <section class="display">
        <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'COMPLETED' && book.user === reader_id)" :key="index">
            <router-link :to="`/book/${userBook.book}`" class="book-link">
                <p class="book-title">Title: {{ books[userBook.book - 1]?.title }}</p>
                <p class="book-author">Author: {{ books[userBook.book - 1]?.author }}</p>
            </router-link>
            <button @click="deleteUserBook(userBook.id)">Delete</button>
        </div>
    </section>
</template>
  
<script lang="ts">
  import { defineComponent } from "vue";
  import { Reader , Book , UserBook} from "../types/index.ts";
  import {useReadersStore} from "../stores/readers.ts"
   import {useReaderStore} from "../stores/reader.ts"
  import {useBooksStore} from "../stores/books.ts"
  import {useUserBooksStore} from "../stores/userBooks.ts"
  import VueCookies from 'vue-cookies';

  export default defineComponent({
    data() {
        return{
            reader_id : Number(window.sessionStorage.getItem("reader_id")),
        }
    },

    async mounted() {
      let response = await fetch("http://localhost:8000/readers/");
      let data = await response.json();
      let readers = data.users as Reader[];
      const store = useReadersStore()
      store.saveReaders(readers)

      let responseBook = await fetch("http://localhost:8000/books/");
      let dataBook = await responseBook.json();
      let books = dataBook.books as Book[];
      const storeBook = useBooksStore()
      storeBook.saveBooks(books)

      let responseUserBook = await fetch("http://localhost:8000/user_books/");
      let dataUserBook = await responseUserBook.json();
      let userBooks = dataUserBook.user_books as UserBook[];
      const storeUserBook = useUserBooksStore()
      storeUserBook.saveUserBooks(userBooks)  
    },
    methods: {
        async updateUserBookStatus(userBook: UserBook, newStatus: string) {
            try {
                const response = await fetch(`http://localhost:8000/user_book/${userBook.id}/`, {
                    method: "PUT",
                    headers: {
                        "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                        "Content-Type": "application/json",
                        "X-CSRFToken": VueCookies.get("csrftoken"),
                    },
                    credentials: "include",
                    body: JSON.stringify({
                        status: newStatus,
                    }),
                });

                if (response.ok) {
                    if (newStatus === "COMPLETED") {
                        // Fetch user data first
                        const userResponse = await fetch(`http://localhost:8000/reader/${this.reader_id}/`, {
                            headers: {
                                "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                                "Content-Type": "application/json",
                            },
                        });

                        if (userResponse.ok) {
                            const userData = await userResponse.json();
                            const updatedBookCount = userData.book_count + 1;

                            // Update user's book count
                            await fetch(`http://localhost:8000/reader/${this.reader_id}/`, {
                                method: "PUT",
                                headers: {
                                    "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                                    "Content-Type": "application/json",
                                    "X-CSRFToken": VueCookies.get("csrftoken"),
                                },
                                credentials: "include",
                                body: JSON.stringify({
                                    book_count: updatedBookCount,
                                }),
                            });
                        }
                    }
                    window.location.reload();
                }
            } catch (error) {
                console.error("Failed to update book status:", error);
            }
        },


        async deleteUserBook(userBookId: number) {
            try {
                 // Find the book to check its status
                const userBook = this.userBooks.find(book => book.id === userBookId);

                const response = await fetch(`http://localhost:8000/user_book/${userBookId}/`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                    "Content-Type": "application/json",
                    "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
                });

                if (!response.ok) throw new Error("Failed to delete user book relationship");

                if (response.ok) {
                    if (userBook && userBook.status === "COMPLETED") {
                        // Fetch user data first
                        const userResponse = await fetch(`http://localhost:8000/reader/${this.reader_id}/`, {
                            headers: {
                                "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                                "Content-Type": "application/json",
                            },
                        });

                        if (userResponse.ok) {
                                const userData = await userResponse.json();
                                const updatedBookCount = Math.max(userData.book_count - 1, 0); // Ensure count doesn't go below 0

                                // Update user's book count
                                await fetch(`http://localhost:8000/reader/${this.reader_id}/`, {
                                    method: "PUT",
                                    headers: {
                                        "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                                        "Content-Type": "application/json",
                                        "X-CSRFToken": VueCookies.get("csrftoken"),
                                    },
                                    credentials: "include",
                                    body: JSON.stringify({
                                        book_count: updatedBookCount,
                                    }),
                                });
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
            const storeBook = useBooksStore();
            return this.storeBook.books;
        },
        userBooks() {
            const storeUserBook = useUserBooksStore();
            return this.storeUserBook.userBooks;
        },
    },
    
    setup() {
        const storeBook = useBooksStore();
        const storeUserBook = useUserBooksStore();
        return {storeBook, storeUserBook};
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

/* Optional Hover Effect for h3 */
h3:hover {
    background: linear-gradient(135deg, #955D5C, #542F2F); /* Inverted gradient on hover */
    transform: scale(1.05); /* Slight zoom effect */
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

/* Optional Hover Effect for Headings */
h2:hover, h3:hover {
    background: linear-gradient(135deg, #955D5C, #542F2F);
    transform: scale(1.05); /* Slight zoom effect */
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
    max-height: 150px; /* Further reduced max height */
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
    color: #f0b400;
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


  