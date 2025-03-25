<template>
  <div class="body">
     <h1>Homepage</h1>
  </div>
  <h2>Books:</h2>
  <section  class="display">
        <div v-for="(book, index) in books" :key="index">
            <router-link :to="`/book/${book.id}`" class="book-link">
                <p>Title: {{ book.title }}</p>
                <p>Author: {{ book.author }}</p>
            </router-link>
        </div>
    </section>
    <h2>Users:</h2>
    <section class="display">

        <div v-for="(reader, index) in filtered_readers" :key="index">
          <router-link :to="`/user/${reader.id}`" class="user-link">
            <p>Username: {{ reader.username }}</p>
          </router-link>
        </div>

    </section>
  
</template>

<script lang="ts">
    import { defineComponent } from "vue";
    import { useReaderStore } from "../stores/reader";
    import { useReadersStore } from "../stores/readers";
    import { useBooksStore } from "../stores/books"
    import { Book, Reader } from "../types/index";
    

    //This home page will display user lists of books
    //It will also display the recommended books and recommended users 
    export default defineComponent({
        data() {
            return {

                reader_id : Number(window.sessionStorage.getItem("reader_id")),

            
            };
        },
        async mounted() {
            // Fetching csrf token using session cookie information on mount
            const sessionCookie = (document.cookie).split(';');
            let currentSessionid: string = ''
            console.log(sessionCookie)
            // Checking in UserStore with CSRF token
            for (let cookie of sessionCookie) {
                cookie = cookie.trim();
                console.log(cookie)
                if (cookie.startsWith("sessionid" + "=")) {
                    currentSessionid = cookie.substring("sessionid".length + 1);
                }
            }
            
            const previousSessionid : string | null = window.sessionStorage.getItem("session_id")
            // Loading values from user store if sessionId matches
            if(currentSessionid == previousSessionid){
                const readerId = Number(window.sessionStorage.getItem("reader_id"));
                try {
                    const readerCookie = await this.readerStore.fetchreaderReturn(Number(window.sessionStorage.getItem("reader_id")));
                    console.log("Fetched User:", readerCookie);
                } catch (error) {
                    console.error("Error fetching user:", error);
                }
            
                console.log('checked sesh')
            }
            else{
                // Extracting user id from url query
                const params = new URLSearchParams(window.location.search);
                const readerId: number = parseInt(params.get("u") || "0");
                console.log(readerId)
                // Fetch user data using url query information on mount
                let reader = await this.readerStore.fetchReaderReturn(readerId);
                console.log(reader)
                this.readerStore.reader = reader;
                // Set session variable
                sessionStorage.setItem("reader_id", readerId.toString());
                
                // Fetching csrf token using session cookie information on mount
                const session_cookie = (document.cookie).split(';');
                console.log(session_cookie)

                //Update user state in UserStore with CSRF token
                for (let cookie of session_cookie) {
                    cookie = cookie.trim();
                    console.log(cookie)
                    if (cookie.startsWith("csrftoken" + "=")) {
                        this.readerStore.setCsrfToken(cookie.substring("csrftoken".length + 1));

                        console.log(this.readerStore.csrf)
                    }
                    //Update sessionStorage state in UserStore with CSRF token
                    console.log(cookie)
                    if (cookie.startsWith("sessionid" + "=")) {
                        // Set session variable
                        let sessionId = cookie.substring("csrftoken".length + 1);
                        sessionStorage.setItem("session_id", sessionId);
                    }
                }
            }

            //gets all of the books
            let responseBook = await fetch("http://localhost:8000/books/");
            let dataBook = await responseBook.json();
            let books = dataBook.books as Book[];
            const storeBook = useBooksStore()
            storeBook.saveBooks(books)

            //gets all of the users
            let responseReader = await fetch("http://localhost:8000/readers/");
            let dataReader = await responseReader.json();
            let readers = dataReader.readers as Reader[];
            console.log(readers)
            const readersStore = useReadersStore()
            readersStore.saveReaders(readers)

        
        },
        methods: {
            
            
        }, 
        computed: {
            readers() {
                const readersStore = useReadersStore();
                return readersStore.readers || []; // Return an empty array if users is undefined
            },
            filtered_readers() {
                  // Ensure users are available before calling filter()
                  if (this.readers.length > 0) {
                      return this.readers.filter(reader => reader.id !== this.reader_id);
                  }
                  return [];  // Return an empty array if users are not loaded
            },
            books() {
                const storeBook = useBooksStore();
                return storeBook.books; 
            },
        },

        setup() {
            const readerStore = useReaderStore();
            const readersStore = useReadersStore();
            const storeBook = useBooksStore();
    
            return { readerStore , readersStore, storeBook };
        },
    });
  </script>


<style scoped>
/* Body Styling */
.body {
    font-family: Arial, Helvetica, sans-serif;
    background-color: #EFE0CB; /* Light background */
    margin: 0;
    padding: 1rem; /* Padding around the body */
    max-height: 75vh; /* Reduce max height to 75% of the viewport height */
    overflow-y: auto; /* Enable scrolling if content overflows */
}

/* Heading Styling */
h1, h2 {
    color: white;
    background-color: #2f4a54; /* Dark background for headers */
    padding: 0.3rem 1rem; /* Reduced padding for better space usage */
    margin: 0.3rem 0; /* Reduced margin between titles */
    border-radius: 5px;
    font-size: 1.6rem; /* Reduced font size for smaller headings */
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1px;
}

h1 {
    font-size: 1.8rem; /* Slightly smaller font for h1 */
    margin-top: 1rem; /* Reduced top margin */
}

h2 {
    font-size: 1.4rem; /* Slightly smaller for h2 */
    margin-top: 0.3rem; /* Smaller top margin for h2 */
}

/* Display Section (Book and User Lists) */
.display {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem; /* Further reduced gap between items */
    justify-content: center; /* Center the items */
    margin-top: 1rem;
    padding: 0 1rem; /* Add padding to prevent stretching on edges */
}

/* General Card Styling for Book and User Items */
.display > div {
    background-color: #2f4a54;
    padding: 0.5rem; /* Reduced padding for compactness */
    margin: 0.3rem; /* Reduced margin */
    border-radius: 8px;
    flex-basis: 30%; /* Adjust card width */
    max-width: 250px; /* Further reduce max-width to 250px */
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.display > div:hover {
    transform: translateY(-4px); /* Slightly smaller hover effect */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Slightly elevated shadow on hover */
}

/* Link Styling */
.book-link, .user-link {
    text-decoration: none;
    color: white;
    font-size: 0.9rem; /* Smaller font size for links */
    font-weight: bold;
    transition: color 0.3s ease, transform 0.3s ease;
}

/* Hover Effect for Links */
.book-link:hover, .user-link:hover {
    color: #f0b400; /* Golden color on hover */
    transform: scale(1.03); /* Slight zoom effect */
}

/* Paragraph Styling (inside links) */
.book-link > p, .user-link > p {
    margin: 0.2rem 0;
    padding: 0.3rem;
    background-color: #71929f; /* Light background for content */
    border-radius: 5px;
    color: white;
    text-align: center;
    font-size: 0.8rem; /* Smaller text size for paragraph */
}

/* Additional Responsive Styling */
@media (max-width: 768px) {
    .display {
        flex-direction: column;
        align-items: center;
    }

    .display > div {
        flex-basis: 80%; /* Increase card width on smaller screens */
        max-width: 100%; /* Allow full width on mobile */
    }

    h1, h2 {
        font-size: 1.4rem; /* Even smaller font for mobile */
    }

    .book-link, .user-link {
        font-size: 0.8rem; /* Smaller font size for mobile */
    }

    .book-link > p, .user-link > p {
        font-size: 0.7rem; /* Even smaller text for mobile */
    }
}


</style>